#include <iostream>
#include <fstream>
#include <vector>
#include <string>
using namespace std;

class Imagem {
public:
    // Matriz de pixels da imagem (R, G, B)
    vector<vector<int>> red, green, blue;
    int width = 0, height = 0, max_value = 255;

    void load_image(string filename) {
        ifstream file(filename, ios::binary);
        if (!file.is_open()) {
            cerr << "Erro ao abrir o arquivo." << endl;
            return;
        }

        // Faz a leitura do File Header do BMP
        char header[54];
        file.read(header, 54);

        // Faz a leitura do Info Header do BMP
        width = *(int*)&header[18];
        height = *(int*)&header[22];
        int size = *(int*)&header[34];

        // Inicializa as matrizes de pixels
        red.resize(width, vector<int>(height));
        green.resize(width, vector<int>(height));
        blue.resize(width, vector<int>(height));

        // Pula os dados desnecessários do BMP
        file.seekg(54, ios::beg);

        // Faz a leitura dos pixels da imagem
        char pixel[4];
        for (int i = 0; i < width * height; i++) {
            file.read(pixel, 3);
            red[i % width][i / width] = (int)pixel[2];
            green[i % width][i / width] = (int)pixel[1];
            blue[i % width][i / width] = (int)pixel[0];
        }

        file.close();
    }

    void save_image(string filename) {
        ofstream file(filename, ios::binary);
        if (!file.is_open()) {
            cerr << "Erro ao abrir o arquivo." << endl;
            return;
        }

        // Faz a escrita da imagem considerando o formato BMP, com 3 canais de cor, width x height pixels
        char header[54] = {
            0x42, 0x4D, 0x36, 0x00, 0x0E, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x36, 0x00, 0x00, 0x00, 0x28, 0x00,
            0x00, 0x00, (char)width, (char)(width >> 8), (char)(width >> 16), (char)(width >> 24),
            (char)height, (char)(height >> 8), (char)(height >> 16), (char)(height >> 24),
            0x01, 0x00, 0x18
        };
        file.write(header, 54);

        // Faz a escrita dos pixels da imagem
        char pixel[4];
        for (int i = 0; i < width * height; i++) {
            pixel[0] = blue[i % width][i / width];
            pixel[1] = green[i % width][i / width];
            pixel[2] = red[i % width][i / width];
            file.write(pixel, 3);
        }

        file.close();

        cout << "Imagem salva com sucesso!" << endl;
    }
};

int main() {
    string image = "drive/MyDrive/convolucao/imagem474.bmp";
    string kernel = "drive/MyDrive/convolucao/kernel_blur.txt";

    Imagem img;
    img.load_image(image);

    img.save_image("saida.bmp");

    return 0;
}
