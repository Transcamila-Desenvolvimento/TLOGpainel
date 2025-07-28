from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Destino, Lancamento, ConfiguracaoDashboard
from .forms import LancamentoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
import openpyxl


def get_tema():
    configuracao, _ = ConfiguracaoDashboard.objects.get_or_create(id=1)
    return configuracao.tema

@login_required
def painel_tv(request):
    destinos = Destino.objects.all()
    data = []
    total_geral = 0
    total_liberado = 0
    total_aguardando = 0

    for destino in destinos:
        lancamentos = destino.lancamento_set.all()

        liberado = lancamentos.filter(status='liberado').aggregate(total=Sum('quantidade'))['total'] or 0
        aguardando = lancamentos.filter(status='aguardando').aggregate(total=Sum('quantidade'))['total'] or 0
        total = liberado + aguardando

        total_liberado += liberado
        total_aguardando += aguardando
        total_geral += total

        data.append({
            'destino_nome': destino.nome,
            'lancamentos': lancamentos,
            'liberado': liberado,
            'aguardando': aguardando,
            'total': total,
        })

    return render(request, 'dashboard.html', {
        'data': data,
        'total_geral': total_geral,
        'total_liberado': total_liberado,
        'total_aguardando': total_aguardando,
        'tema': get_tema(),
    })

@login_required
def lancamento_list(request):
    lancamentos = Lancamento.objects.select_related('destino').all().order_by('-criado_em')
    lancamentos_liberados = lancamentos.filter(status='liberado')
    lancamentos_aguardando = lancamentos.filter(status='aguardando')
    destinos = Destino.objects.all()

    context = {
        'lancamentos': lancamentos,
        'total_liberado': lancamentos_liberados.count(),
        'lancamentos_aguardando': lancamentos_aguardando,
        'destinos': destinos,
        'tema': get_tema(),
    }

    return render(request, 'lancamento_list.html', context)

@login_required
def lancamento_create(request):
    if request.method == 'POST':
        form = LancamentoForm(request.POST)
        if form.is_valid():
            lancamento = form.save(commit=False)
            lancamento.criado_por = request.user
            lancamento.save()
            return redirect('lancamento_list')
    else:
        form = LancamentoForm()

    return render(request, 'lancamento_form.html', {'form': form, 'tema': get_tema()})

@login_required
def lancamento_update(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk)
    
    if request.method == 'POST':
        form = LancamentoForm(request.POST, instance=lancamento)
        if form.is_valid():
            updated_lancamento = form.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                data = {
                    'success': True,
                    'message': 'Processo atualizado com sucesso!',
                    'lancamento': {
                        'id': updated_lancamento.id,
                        'po': updated_lancamento.po,
                        'destino': {
                            'id': updated_lancamento.destino.id,
                            'nome': updated_lancamento.destino.nome
                        },
                        'quantidade': updated_lancamento.quantidade,
                        'status': updated_lancamento.status,
                        'observacao': updated_lancamento.observacao,
                        'criado_em': updated_lancamento.criado_em.strftime('%d/%m/%Y')
                    }
                }
                return JsonResponse(data)
            
            return redirect('lancamento_list')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {field: error[0] for field, error in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    form = LancamentoForm(instance=lancamento)
    return render(request, 'lancamento_form.html', {'form': form, 'tema': get_tema()})

@login_required
def lancamento_delete(request, pk):
    lancamento = get_object_or_404(Lancamento, pk=pk)
    if request.method == 'POST':
        lancamento_id = lancamento.id
        lancamento.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Processo excluído com sucesso!',
                'lancamento_id': lancamento_id
            })
        
        return redirect('lancamento_list')
    
    return render(request, 'lancamento_confirm_delete.html', {
        'lancamento': lancamento,
        'tema': get_tema()
    })

@login_required
def configuracoes(request):
    configuracao, _ = ConfiguracaoDashboard.objects.get_or_create(id=1)

    if request.method == "POST":
        tema = request.POST.get("tema")
        if tema in ["claro", "escuro", "azul"]:
            configuracao.tema = tema
            configuracao.save()
        return redirect("configuracoes")

    return render(request, "configuracoes.html", {"tema": configuracao.tema})

def exportar_processos(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Processos"

    # Cabeçalho com nova coluna
    ws.append(['Processo', 'Destino', 'Quantidade', 'Data de criação', 'Status', 'Observação', 'Criado por'])

    lancamentos = Lancamento.objects.all()
    for l in lancamentos:
        ws.append([
            l.po,
            l.destino.nome,
            l.quantidade,
            l.criado_em.strftime("%d/%m/%Y"),
            l.status,
            l.observacao,
            l.criado_por.get_full_name() if l.criado_por else '—'  # Nome completo ou '—'
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=processos.xlsx'
    wb.save(response)
    return response

def check_po_exists(request):
    po = request.GET.get('po', '')
    exists = Lancamento.objects.filter(po=po).exists()
    return JsonResponse({'exists': exists})