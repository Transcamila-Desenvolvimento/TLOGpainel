# 📱 Como Configurar WebView para Notificações Push

Este guia mostra como configurar um WebView no Android e iOS para que as notificações push funcionem corretamente.

---

## ⚠️ REQUISITOS IMPORTANTES

### 1. HTTPS é OBRIGATÓRIO
- ❌ **NÃO funciona** em HTTP (exceto localhost)
- ✅ **Funciona** apenas em HTTPS ou localhost
- Use um servidor HTTPS para produção: `https://seudominio.com.br`

### 2. Service Workers
- Service Workers são necessários para notificações push
- Já estão configurados no sistema, mas o WebView precisa permitir

---

## 🤖 ANDROID (Java/Kotlin)

### **Opção 1: WebView nativo (Recomendado)**

#### **1. Adicionar Permissões no AndroidManifest.xml**

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    
    <!-- Permissões necessárias -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    
    <application
        android:usesCleartextTraffic="false"
        ...>
        
        <activity
            android:name=".MainActivity"
            ...>
        </activity>
    </application>
</manifest>
```

#### **2. Configurar WebView no Java/Kotlin**

**Java:**
```java
import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends Activity {
    private static final int REQUEST_CODE_NOTIFICATIONS = 1001;
    private WebView webView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        webView = findViewById(R.id.webView);
        
        // Configurar WebView
        WebSettings webSettings = webView.getSettings();
        
        // OBRIGATÓRIO: Habilitar JavaScript
        webSettings.setJavaScriptEnabled(true);
        
        // OBRIGATÓRIO: Habilitar Dom Storage (necessário para Service Workers)
        webSettings.setDomStorageEnabled(true);
        
        // Habilitar outras funcionalidades úteis
        webSettings.setDatabaseEnabled(true);
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
        webSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE);
        
        // OBRIGATÓRIO: Permitir que Service Workers funcionem
        webSettings.setJavaScriptCanOpenWindowsAutomatically(true);
        
        // Configurar WebChromeClient para pedir permissões
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onPermissionRequest(PermissionRequest request) {
                // Se for permissão de notificações
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    // Android 13+ precisa de permissão POST_NOTIFICATIONS
                    if (ContextCompat.checkSelfPermission(MainActivity.this, 
                            Manifest.permission.POST_NOTIFICATIONS) 
                            != PackageManager.PERMISSION_GRANTED) {
                        ActivityCompat.requestPermissions(MainActivity.this,
                                new String[]{Manifest.permission.POST_NOTIFICATIONS},
                                REQUEST_CODE_NOTIFICATIONS);
                    }
                }
                // Sempre conceder a permissão do WebView
                request.grant(request.getResources());
            }
        });
        
        // Solicitar permissão de notificações no Android 13+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, 
                    Manifest.permission.POST_NOTIFICATIONS) 
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.POST_NOTIFICATIONS},
                        REQUEST_CODE_NOTIFICATIONS);
            }
        }
        
        // Carregar a URL do sistema
        String url = "https://seudominio.com.br"; // OU "http://localhost:8000" para desenvolvimento
        webView.loadUrl(url);
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_CODE_NOTIFICATIONS) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permissão concedida, recarregar página
                webView.reload();
            }
        }
    }
    
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
```

**Kotlin:**
```kotlin
import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

class MainActivity : AppCompatActivity() {
    private val REQUEST_CODE_NOTIFICATIONS = 1001
    private lateinit var webView: WebView
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        webView = findViewById(R.id.webView)
        
        // Configurar WebView
        val webSettings = webView.settings
        
        // OBRIGATÓRIO: Habilitar JavaScript
        webSettings.javaScriptEnabled = true
        
        // OBRIGATÓRIO: Habilitar Dom Storage (necessário para Service Workers)
        webSettings.domStorageEnabled = true
        
        // Habilitar outras funcionalidades
        webSettings.databaseEnabled = true
        webSettings.cacheMode = WebSettings.LOAD_DEFAULT
        webSettings.mixedContentMode = WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
        
        // OBRIGATÓRIO: Permitir Service Workers
        webSettings.javaScriptCanOpenWindowsAutomatically = true
        
        // Configurar WebChromeClient para pedir permissões
        webView.webChromeClient = object : WebChromeClient() {
            override fun onPermissionRequest(request: PermissionRequest) {
                // Android 13+ precisa de permissão POST_NOTIFICATIONS
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    if (ContextCompat.checkSelfPermission(this@MainActivity,
                            Manifest.permission.POST_NOTIFICATIONS)
                            != PackageManager.PERMISSION_GRANTED) {
                        ActivityCompat.requestPermissions(this@MainActivity,
                                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                                REQUEST_CODE_NOTIFICATIONS)
                    }
                }
                // Sempre conceder a permissão do WebView
                request.grant(request.resources)
            }
        }
        
        // Solicitar permissão de notificações no Android 13+
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this,
                    Manifest.permission.POST_NOTIFICATIONS)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                        arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                        REQUEST_CODE_NOTIFICATIONS)
            }
        }
        
        // Carregar a URL do sistema
        val url = "https://seudominio.com.br" // OU "http://localhost:8000" para desenvolvimento
        webView.loadUrl(url)
    }
    
    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_CODE_NOTIFICATIONS) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permissão concedida, recarregar página
                webView.reload()
            }
        }
    }
    
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
```

#### **3. Layout XML (activity_main.xml)**

```xml
<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical">
    
    <WebView
        android:id="@+id/webView"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
    
</LinearLayout>
```

---

## 🍎 iOS (Swift)

### **1. Adicionar Permissões no Info.plist**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Descrição para permissão de notificações -->
    <key>NSUserNotificationsUsageDescription</key>
    <string>Precisamos de permissão para enviar notificações sobre processos e agendamentos.</string>
    
    <!-- Permitir HTTP em desenvolvimento (remover em produção) -->
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <true/>
    </dict>
</dict>
</plist>
```

### **2. Configurar WKWebView no Swift**

```swift
import UIKit
import WebKit
import UserNotifications

class ViewController: UIViewController, WKNavigationDelegate {
    @IBOutlet weak var webView: WKWebView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Configurar WebView
        let configuration = WKWebViewConfiguration()
        
        // OBRIGATÓRIO: Permitir Service Workers
        if #available(iOS 14.0, *) {
            configuration.defaultWebpagePreferences.allowsContentJavaScript = true
        }
        
        // Configurações úteis
        configuration.allowsInlineMediaPlayback = true
        configuration.mediaTypesRequiringUserActionForPlayback = []
        configuration.processPool = WKProcessPool()
        
        // Criar WebView
        if webView == nil {
            webView = WKWebView(frame: view.bounds, configuration: configuration)
            webView.navigationDelegate = self
            view.addSubview(webView)
            
            // Auto Layout
            webView.translatesAutoresizingMaskIntoConstraints = false
            NSLayoutConstraint.activate([
                webView.topAnchor.constraint(equalTo: view.topAnchor),
                webView.leadingAnchor.constraint(equalTo: view.leadingAnchor),
                webView.trailingAnchor.constraint(equalTo: view.trailingAnchor),
                webView.bottomAnchor.constraint(equalTo: view.bottomAnchor)
            ])
        }
        
        // Solicitar permissão de notificações
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound, .badge]) { granted, error in
            if granted {
                print("✅ Permissão de notificações concedida")
                // Registrar para notificações remotas (se necessário)
                DispatchQueue.main.async {
                    UIApplication.shared.registerForRemoteNotifications()
                }
            } else {
                print("❌ Permissão de notificações negada")
            }
        }
        
        // Carregar a URL do sistema
        if let url = URL(string: "https://seudominio.com.br") { // OU "http://localhost:8000" para desenvolvimento
            let request = URLRequest(url: url)
            webView.load(request)
        }
    }
    
    // MARK: - WKNavigationDelegate
    
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        print("✅ Página carregada")
    }
    
    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        print("❌ Erro ao carregar página: \(error.localizedDescription)")
    }
}
```

**⚠️ IMPORTANTE no iOS:**
- Service Workers só funcionam a partir do iOS 16.4+ (Safari 16.4+)
- Em versões anteriores, as notificações push podem não funcionar

---

## ⚡ React Native (Alternativa)

Se estiver usando React Native, você pode usar `react-native-webview`:

```bash
npm install react-native-webview
```

```javascript
import React, { useEffect } from 'react';
import { View, PermissionsAndroid, Platform } from 'react-native';
import { WebView } from 'react-native-webview';

const App = () => {
  useEffect(() => {
    // Solicitar permissão de notificações no Android
    if (Platform.OS === 'android') {
      requestNotificationPermission();
    }
  }, []);

  const requestNotificationPermission = async () => {
    if (Platform.VERSION >= 33) {
      try {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS
        );
        if (granted === PermissionsAndroid.RESULTS.GRANTED) {
          console.log('✅ Permissão de notificações concedida');
        }
      } catch (err) {
        console.warn('Erro ao solicitar permissão:', err);
      }
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <WebView
        source={{ uri: 'https://seudominio.com.br' }}
        javaScriptEnabled={true}
        domStorageEnabled={true}
        allowsInlineMediaPlayback={true}
        mixedContentMode="compatibility"
        onPermissionRequest={(request) => {
          // Conceder todas as permissões solicitadas
          request.grant(request.getResources());
        }}
      />
    </View>
  );
};

export default App;
```

---

## ✅ Checklist de Configuração

### **Android:**
- [ ] Permissão `INTERNET` no AndroidManifest.xml
- [ ] Permissão `POST_NOTIFICATIONS` no AndroidManifest.xml (Android 13+)
- [ ] `setJavaScriptEnabled(true)` no WebView
- [ ] `setDomStorageEnabled(true)` no WebView
- [ ] `setJavaScriptCanOpenWindowsAutomatically(true)` no WebView
- [ ] WebChromeClient configurado com `onPermissionRequest`
- [ ] Solicitar permissão POST_NOTIFICATIONS no código (Android 13+)

### **iOS:**
- [ ] `NSUserNotificationsUsageDescription` no Info.plist
- [ ] WKWebView com JavaScript habilitado
- [ ] Solicitar permissão com `UNUserNotificationCenter`
- [ ] iOS 16.4+ para Service Workers funcionarem

### **Ambos:**
- [ ] URL usando HTTPS (ou localhost para desenvolvimento)
- [ ] Usuário ativou notificações no sistema web (dentro do WebView)

---

## 🧪 Testar no WebView

1. **Abra o app** com o WebView configurado
2. **Faça login** no sistema
3. **Vá em "Configurações e Perfil"**
4. **Ative as notificações push** (mesmo processo do navegador)
5. **Permita** quando o WebView pedir permissão
6. **Teste** executando `python testar_push_localhost.py` (se estiver em desenvolvimento)

---

## 📝 Notas Importantes

1. **HTTPS obrigatório em produção** - Web Push não funciona em HTTP
2. **Service Workers precisam ser habilitados** no WebView
3. **Permissões do sistema** - Android 13+ e iOS precisam de permissões explícitas
4. **Teste sempre** - Certifique-se de testar as notificações após implementar

---

## 🔧 Troubleshooting

### **Notificações não aparecem no Android:**
- Verifique se `POST_NOTIFICATIONS` está no AndroidManifest.xml
- Verifique se a permissão foi concedida no código
- Verifique se `domStorageEnabled` está `true`
- Verifique se está usando HTTPS (não funciona em HTTP exceto localhost)

### **Notificações não aparecem no iOS:**
- Verifique se `NSUserNotificationsUsageDescription` está no Info.plist
- Verifique se a versão do iOS é 16.4+ (para Service Workers)
- Verifique se a permissão foi solicitada e concedida
- Verifique se está usando HTTPS

---

## 📞 Precisa de Ajuda?

Se tiver problemas:
1. Verifique os logs do app (Android Studio / Xcode)
2. Verifique o console do navegador no WebView (use `chrome://inspect` no Android)
3. Teste primeiro no navegador desktop para garantir que funciona
4. Certifique-se que o backend está enviando as notificações corretamente

