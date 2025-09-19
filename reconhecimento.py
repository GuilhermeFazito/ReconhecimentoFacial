import cv2
import dlib
import numpy as np
import pickle
import os

# Detector e modelos
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
face_rec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

DB_FILE = "faces_db.pkl"

# Carregar banco de dados
if os.path.exists(DB_FILE):
    with open(DB_FILE, "rb") as f:
        faces_db = pickle.load(f)
else:
    faces_db = {}

cap = cv2.VideoCapture(0)

# Configurações do oval fixo
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center = (frame_width // 2, frame_height // 2)
axes = (150, 200)  # tamanho do oval

print("Pressione [ESPACO] para cadastrar usuário, [ESC] para sair.")

def mostrar_tela_xperiencia(nome):
    #exibiçao da tela da XPeriencia
    screen = np.full((frame_height, frame_width, 3), (0, 255, 0), dtype=np.uint8)

    # Texto da primeira linha
    texto1 = "Bem-vindo a XPeriencia"
    (tw1, th1), _ = cv2.getTextSize(texto1, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
    x1 = (frame_width - tw1) // 2
    y1 = frame_height // 2 - 40
    cv2.putText(screen, texto1, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

    # Texto da segunda linha
    (tw2, th2), _ = cv2.getTextSize(nome, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
    x2 = (frame_width - tw2) // 2
    y2 = frame_height // 2 + 40
    cv2.putText(screen, nome, (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

    while True:
        cv2.imshow("XPeriencia", screen)
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            cv2.destroyWindow("XPeriencia")
            break

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fim do vídeo ou erro na captura.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    # captura oval fixa
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)

    fundo_verde = np.full(frame.shape, (0, 50, 0), dtype=np.uint8)
    frame = np.where(mask[:, :, np.newaxis] == 255, frame, fundo_verde)
    cv2.ellipse(frame, center, axes, 0, 0, 360, (0, 0, 255), 2)

    embedding = None
    nome_user = "Desconhecido"

    for face in faces:
        x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
        face_center = ((x1 + x2) // 2, (y1 + y2) // 2)

        if ((face_center[0] - center[0])**2 / axes[0]**2 +
            (face_center[1] - center[1])**2 / axes[1]**2) <= 1:
            shape = predictor(frame, face)
            face_descriptor = face_rec.compute_face_descriptor(frame, shape)
            embedding = np.array(face_descriptor)

            # Comparar com DB
            for nome, emb in faces_db.items():
                dist = np.linalg.norm(emb - embedding)
                if dist < 0.6:
                    nome_user = nome
                    break

    # Mostra o nome (Desconhecido) no canto
    cv2.putText(frame, nome_user, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.imshow("Reconhecimento Facial", frame)
    key = cv2.waitKey(1)

    # Cadastrar usuário
    if key == 32 and embedding is not None:  # ESPAÇO
        nome = input("Digite o nome para cadastrar: ")
        if nome in faces_db:
            print(f"⚠️ O usuário '{nome}' já está cadastrado.")
        else:
            faces_db[nome] = embedding
            with open(DB_FILE, "wb") as f:
                pickle.dump(faces_db, f)
            print(f"✅ {nome} cadastrado com sucesso!")

            # Fecha a câmera antes de mostrar a tela 
            cap.release()
            cv2.destroyWindow("Reconhecimento Facial")

            # Tela verde até  apertar ESC
            mostrar_tela_xperiencia(nome)

            # Reabre a câmera após fechar a tela
            cap = cv2.VideoCapture(0)

    # Verifica automatico
    elif embedding is not None and nome_user != "Desconhecido":
        # Fecha a câmera antes de mostrar a tela XPeriencia
        cap.release()
        cv2.destroyWindow("Reconhecimento Facial")

        mostrar_tela_xperiencia(nome_user)

        # Reabre a câmera depois de fechar a tela
        cap = cv2.VideoCapture(0)

    # Sair
    elif key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
