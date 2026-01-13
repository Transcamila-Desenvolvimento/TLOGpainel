/**
 * Sistema de Smart Update (Adaptive Long Polling)
 * Otimizado para PythonAnywhere: "Instantâneo" quando ativo, "Lento" quando ocioso.
 */

const SmartUpdate = {
    tela: null, // 'portaria', 'checklist', 'onda', 'armazem', 'liberacao-documentos'
    timestamp: null, // Última atualização recebida do servidor
    timer: null,

    // Controle de Atividade
    isUserActive: true,
    lastActivityTime: Date.now(),
    idleThreshold: 60000, // 60 segundos para considerar ocioso

    // Intervalos (ms)
    intervals: {
        active: 3000,      // 3s (Sensação Instantânea)
        idle: 10000,       // 10s (Economia 70%)
        hidden: 30000,     // 30s (Tab em segundo plano - Economia 90%)
        error: 20000       // 20s (Se der erro no server, acalma)
    },

    init: function (tela) {
        this.tela = tela;
        console.log(`🚀 Smart Update Adaptive iniciado para: ${tela}`);

        // Inicializar rastreadores de atividade
        this.setupActivityTrackers();

        // Começar o loop
        this.scheduleNext(1000); // 1s delay inicial
    },

    setupActivityTrackers: function () {
        const resetActivity = () => {
            if (!this.isUserActive) {
                // Se estava inativo e voltou, força update rápido pra atualizar a tela
                console.log("👋 Usuário voltou! Acelerando updates...");
                this.isUserActive = true;
                // Opcional: reiniciar loop imediatamente? 
                // Melhor deixar o próximo ciclo pegar o novo intervalo curto.
            }
            this.lastActivityTime = Date.now();
        };

        // Eventos que indicam presença do usuário
        ['mousemove', 'keydown', 'click', 'scroll', 'touchstart'].forEach(evt => {
            window.addEventListener(evt, resetActivity, { passive: true });
        });
    },

    getInterval: function () {
        const now = Date.now();

        // 1. Prioridade: Se houve erro recente (implementado no catch)

        // 2. Se a aba está oculta (background)
        if (document.hidden) {
            return this.intervals.hidden;
        }

        // 3. Verificar ociosidade
        if (now - this.lastActivityTime > this.idleThreshold) {
            this.isUserActive = false;
            return this.intervals.idle;
        }

        // 4. Modo Ativo (Padrão)
        return this.intervals.active;
    },

    scheduleNext: function (ms) {
        if (this.timer) clearTimeout(this.timer);
        this.timer = setTimeout(() => this.checkUpdates(), ms);
    },

    checkUpdates: function () {
        const currentInterval = this.getInterval();

        // Params para request
        const params = new URLSearchParams({
            tela: this.tela,
            timestamp: this.timestamp || '',
            _: new Date().getTime() // Cache buster
        });

        fetch(`/rondonopolis/api/verificar-atualizacoes/?${params.toString()}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                if (data.update) {
                    console.log(`✨ [SmartUpdate] Atualizando... (${currentInterval}ms)`);
                    this.timestamp = data.timestamp; // Atualiza timestamp local
                    this.refreshTable();
                    // refreshTable vai agendar o próximo quando terminar
                } else {
                    if (data.timestamp && !this.timestamp) {
                        this.timestamp = data.timestamp; // Sync inicial
                    }
                    // Nada novo, agendar próximo
                    this.scheduleNext(currentInterval);
                }
            })
            .catch(error => {
                console.warn('⚠️ Erro no Polling (Servidor ocupado ou offline):', error);
                // Backoff em caso de erro
                this.scheduleNext(this.intervals.error);
            });
    },

    refreshTable: function () {
        fetch(`/rondonopolis/${this.tela}/tabela/?_=${new Date().getTime()}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');

                // Mapeamentos de containers por tela
                if (this.tela === 'portaria') {
                    this.updateContainer('conteudo-agendados', doc);
                    this.updateContainer('conteudo-liberados', doc);
                    this.updateContainer('tab-agendados', doc);
                    this.updateContainer('tab-liberados', doc);
                } else if (this.tela === 'checklist') {
                    this.updateContainer('conteudo-pendentes', doc);
                    this.updateContainer('conteudo-concluidos', doc);
                    this.updateContainer('badge-pendentes', doc);
                    this.updateContainer('badge-concluidos', doc);
                } else if (this.tela === 'onda') {
                    this.updateContainer('conteudo-pendentes', doc);
                    this.updateContainer('conteudo-confirmados', doc);
                    this.updateContainer('badge-pendentes', doc);
                    this.updateContainer('badge-confirmados', doc);
                } else if (this.tela === 'armazem') {
                    this.updateContainer('conteudo-pendentes', doc);
                    this.updateContainer('conteudo-confirmados', doc);
                    this.updateContainer('badge-pendentes', doc);
                    this.updateContainer('badge-confirmados', doc);
                } else if (this.tela === 'liberacao-documentos') {
                    this.updateContainer('conteudo-pendentes', doc);
                    this.updateContainer('conteudo-confirmados', doc);
                    this.updateContainer('badge-pendentes', doc);
                    this.updateContainer('badge-confirmados', doc);
                }
            })
            .catch(err => console.error('❌ Erro no refresh HTML:', err))
            .finally(() => {
                // IMPORTANTE: Só agendar o próximo depois que terminar de renderizar
                this.scheduleNext(this.getInterval());
            });
    },

    updateContainer: function (id, newDoc) {
        const currentEl = document.getElementById(id);
        const newEl = newDoc.getElementById(id);

        if (currentEl && newEl) {
            currentEl.innerHTML = newEl.innerHTML;
            if (currentEl.hasAttribute('data-badge')) {
                currentEl.textContent = newEl.textContent;
            }
            // Animação de flash discreta para indicar update? (Opcional)
            // currentEl.style.opacity = 0.5;
            // setTimeout(() => currentEl.style.opacity = 1, 300);
        }
    },

    // Função para chamar manualmente após uma ação do usuário (Ex: clicou em salvar)
    forceCheck: function () {
        console.log("⚡ Forçando update manual");
        this.scheduleNext(100);
    }
};

// Expor globalmente para ser chamado por outros scripts
window.SmartUpdate = SmartUpdate;
