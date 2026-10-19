# PS5 App

Aplicativo Android Kivy para localizar o PS5 na rede local e abrir os serviços:

- Prospero Manager: `http://IP_DO_PS5:7070/`
- Payload Manager: `http://IP_DO_PS5:8084/`

## Gerar APK no GitHub

1. Envie estes arquivos ao repositório.
2. Abra **Actions**.
3. Selecione **Build APK** e execute **Run workflow**, ou faça um commit para disparar automaticamente.
4. Quando terminar com sucesso, abra a execução e baixe o artefato `ps5app-apk`.

O workflow usa `actions/checkout@v5` e `actions/setup-python@v6` para evitar as versões antigas de runtime Node.js.

Nota: a busca automática depende de o PS5 e o celular estarem na mesma rede/sub-rede e de o roteador permitir tráfego local. Os serviços nas portas 7070 e 8084 precisam estar ativos no PS5.
