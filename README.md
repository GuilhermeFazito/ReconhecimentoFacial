# 👤 Sistema de Reconhecimento Facial para Autenticação

## 🎯 Objetivo
Este projeto tem como objetivo implementar um sistema de autenticação por **reconhecimento facial**, oferecendo uma alternativa mais segura e personalizada em comparação ao uso tradicional de login e senha.  

Ele utiliza as bibliotecas **OpenCV** e **dlib** para detecção de rostos, extração de pontos faciais e geração de vetores de reconhecimento, que são comparados com um banco de dados local.

---

## ⚙️ Dependências
Antes de executar o projeto, instale as dependências necessárias.  
No terminal da sua IDE, execute:  

```
python -m pip install cmake dlib-bin opencv-python matplotlib
```


▶️ Execução
1. Clone ou baixe este repositório em sua máquina.
2. Abra o projeto na sua IDE de preferência (ex.: VS Code, PyCharm).
3. Certifique-se de estar com a câmera habilitada, pois o sistema depende dela para capturar o rosto.

🔧 Parâmetros de Funcionamento
O sistema compara vetores faciais para identificar usuários.
Caso a distância entre vetores seja menor que 0.6, o usuário é considerado reconhecido.
Tecla espaço → permite cadastrar um novo usuário.
Reconhecimento bem-sucedido → exibe a tela de boas-vindas da aplicação.

⚖️ Nota Ética
O uso de dados faciais envolve questões sérias de privacidade e segurança.
Este projeto é apenas para fins acadêmicos e de aprendizado.
Os dados faciais são armazenados localmente e não devem ser compartilhados sem o consentimento explícito dos usuários.
Qualquer uso em ambiente real deve seguir normas da LGPD (Lei Geral de Proteção de Dados) e outras legislações aplicáveis.