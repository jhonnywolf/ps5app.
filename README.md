# PS5 Hub para Android

Este projeto cria um APK Android que abre https://jhonnywolf.github.io/ps5hub/ em uma WebView, com JavaScript, armazenamento local, seletor de arquivos e downloads.

## Gerar o APK pelo GitHub Actions

1. Crie um repositório novo no GitHub (por exemplo `ps5hub-android`).
2. Extraia este ZIP e envie **o conteúdo** para a raiz do repositório.
3. Abra a aba **Actions** e habilite workflows, se o GitHub solicitar.
4. Entre em **Build PS5 Hub APK** e clique em **Run workflow** (ou faça um push na branch `main`/`master`).
5. Quando terminar com sucesso, abra a execução e baixe o artefato **PS5Hub-debug-apk**.
6. Extraia o ZIP do artefato e instale `app-debug.apk` no Android.

## Observações
- É um APK de depuração, não assinado para publicação na Play Store.
- O aplicativo precisa de internet para carregar o site.
- O conteúdo do site é carregado do endereço online; não é uma cópia offline do repositório.
- Revise o conteúdo do site e só use payloads/arquivos que você confia.
