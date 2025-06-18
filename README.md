# 🎛️ Controle de Volume com Gestos

Este projeto utiliza **visão computacional** e **técnicas de inteligência artificial** para controlar o volume do sistema operacional através de 
**gestos com as mãos capturados pela webcam**. Ele também implementa um sistema de **mute/desmute** baseado na abertura ou fechamento da mão.

## ✨ Funcionalidades

- Controle contínuo de volume com base na distância entre o **dedo indicador** e o **polegar**.
- Modo **mute automático** ao fechar completamente a mão.
- Desmute automático ao abrir completamente a mão.
- Interface em tempo real com feedback visual.

## 🧠 Técnicas de IA Utilizadas

O projeto faz uso de **MediaPipe Hands**, um modelo pré-treinado de detecção e rastreamento de mãos, desenvolvido pelo Google. Essa ferramenta utiliza:

- **Detecção de pontos chave (landmarks)** da mão em tempo real.
- Reconhecimento de gestos através da posição relativa dos dedos.
- Rastreio eficiente que permite inferência em tempo real sem necessidade de modelos personalizados.

## 🛠️ Tecnologias Utilizadas

- OpenCV – Para captura e exibição de vídeo.
- MediaPipe– Para rastreamento e reconhecimento de mão.
- pycaw– Para controle do volume no Windows.
- Python 3.8+
## 📸 Imagens e Vídeo da Aplicação em Funcionamento
![Som Ativo](https://github.com/user-attachments/assets/a07fd8af-c896-41ef-8c18-2b3f2fbc3d22)
![Mutado](https://github.com/user-attachments/assets/b5272472-1603-4b06-a68d-383a299c6b90)
![Controle Volume](https://github.com/user-attachments/assets/72db81f9-d11e-4fb1-84f4-a0a9f5d76c7d)

## 🎥  Vídeo
https://github.com/user-attachments/assets/69bb9f8c-ebbc-482d-b9ce-0900f14b0ae4

