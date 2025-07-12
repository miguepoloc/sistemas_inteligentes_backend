# train_model.py
import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from extract_embeddings import get_embedding

DATA_PATH = "data"

class AudioDataset(Dataset):
    def __init__(self, data_path):
        self.samples = []
        for label in os.listdir(data_path):
            label_path = os.path.join(data_path, label)
            if os.path.isdir(label_path):
                for fname in os.listdir(label_path):
                    if fname.lower().endswith(".wav"):
                        self.samples.append((os.path.join(label_path, fname), int(label)))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        emb = get_embedding(path)
        # Asegurar tipo correcto
        return emb[0].float(), torch.tensor(label, dtype=torch.long)

class SimpleClassifier(nn.Module):
    def __init__(self, input_dim, num_classes):
        super().__init__()
        self.fc = nn.Linear(input_dim, num_classes)

    def forward(self, x):
        return self.fc(x)

def train():
    dataset = AudioDataset(DATA_PATH)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    input_dim = 768  # Wav2Vec2 base output size
    num_classes = len(os.listdir(DATA_PATH))
    model = SimpleClassifier(input_dim, num_classes)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(17):
        total_loss = 0
        for x, y in dataloader:
            x = x.float()  # [batch_size, input_dim]
            y = y.long()   # [batch_size]

            # 🧪 Verificar formas reales
            print(f"x shape: {x.shape}, y shape: {y.shape}")

            out = model(x)  # → debe ser [batch_size, num_classes]
            print(f"out shape: {out.shape}")  # 🧪 imprimir shape

            loss = criterion(out, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"📘 Epoch {epoch+1}, Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), "clasificador_audio.pt")
    print("✅ Modelo guardado como clasificador_audio.pt")

if __name__ == "__main__":
    train()
