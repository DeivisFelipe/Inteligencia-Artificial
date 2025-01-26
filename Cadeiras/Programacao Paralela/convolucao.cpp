%%gpu
#include <fstream> // Leitura de arquivos
#include <vector> // Vetores
#include <string> // Strings
#include <stdexcept> // Exceções
#include <iostream> // Entrada e saída
#include <stdint.h> // Tipos inteiros

using namespace std;

// Estrutura de um arquivo BMP
// Pragma pack é utilizado para garantir que a estrutura tenha o tamanho correto
#pragma pack(push, 1)

// Estrutura do cabeçalho de um arquivo BMP
struct BMPFileHeader {
    uint16_t file_type{ 0x4D42 };          // Fala que é um arquivo BMP
    uint32_t file_size{ 0 };               // Tamanho do arquivo em bytes
    uint16_t reserved1{ 0 };               // Reservado, sempre 0
    uint16_t reserved2{ 0 };               // Reservado, sempre 0
    uint32_t offset_data{ 0 };             // Offset para o início dos dados
};

// Estrutura do cabeçalho de informação de um arquivo BMP
struct BMPInfoHeader {
    uint32_t size{ 0 };                      // Tamanho do cabeçalho de informação
    int32_t width{ 0 };                      // Largura da imagem em pixels
    int32_t height{ 0 };                     // Altura da imagem em pixels
                                             //       (se positivo, bottom-up, com origem no canto inferior esquerdo)
                                             //       (se negativo, top-down, com origem no canto superior esquerdo)
    uint16_t planes{ 1 };                    // Número de planos de cor
    uint16_t bit_count{ 0 };                 // Número de bits por pixel
    uint32_t compression{ 0 };               // 0 or 3 - sem compressão, apenas sem compressão suportada
    uint32_t size_image{ 0 };                // 0 - para imagens sem compressão
    int32_t x_pixels_per_meter{ 0 };         // Resolução horizontal da imagem
    int32_t y_pixels_per_meter{ 0 };         // Resolução vertical da imagem
    uint32_t colors_used{ 0 };               // Número de cores na paleta, Use 0 para cores máximas permitidas pelo bit_count
    uint32_t colors_important{ 0 };          // Número de cores importantes, geralmente 0
};

// Estrutura do cabeçalho de cor de um arquivo BMP
// Usado apenas para imagens transparentes
struct BMPColorHeader {
    uint32_t red_mask{ 0x00ff0000 };         // Máscara de bits para o canal vermelho
    uint32_t green_mask{ 0x0000ff00 };       // Máscara de bits para o canal verde
    uint32_t blue_mask{ 0x000000ff };        // Máscara de bits para o canal azul
    uint32_t alpha_mask{ 0xff000000 };       // Máscara de bits para o canal alfa
    uint32_t color_space_type{ 0x73524742 }; // Tipo de espaço de cor sRGB (sRGB)
    uint32_t unused[16]{ 0 };                // Não utilizado, deve ser 0
};
#pragma pack(pop)

// Estrutura de um arquivo BMP
struct BMP {
    BMPFileHeader file_header; // Cabeçalho do arquivo
    BMPInfoHeader bmp_info_header; // Cabeçalho de informação
    BMPColorHeader bmp_color_header; // Cabeçalho de cor
    vector<uint8_t> data; // Dados da imagem
    string image_name; // Nome da imagem

    // Construtor que lê uma imagem BMP de um arquivo
    BMP(string image_name) : image_name(image_name) {
        ifstream inp{ image_name.c_str(), ios_base::binary };
        if (inp) {
            inp.read((char*)&file_header, sizeof(file_header));
            if(file_header.file_type != 0x4D42) {
                throw runtime_error("Error! Unrecognized file format.");
            }
            inp.read((char*)&bmp_info_header, sizeof(bmp_info_header));

            // The BMPColorHeader is used only for transparent images
            if(bmp_info_header.bit_count == 32) {
                // Check if the file has bit mask color information
                if(bmp_info_header.size >= (sizeof(BMPInfoHeader) + sizeof(BMPColorHeader))) {
                    inp.read((char*)&bmp_color_header, sizeof(bmp_color_header));
                    // Check if the pixel data is stored as BGRA and if the color space type is sRGB
                    check_color_header(bmp_color_header);
                } else {
                    cerr << "Error! The file \"" << image_name.c_str() << "\" does not seem to contain bit mask information\n";
                    throw runtime_error("Error! Unrecognized file format.");
                }
            }

            // Jump to the pixel data location
            inp.seekg(file_header.offset_data, inp.beg);

            // Adjust the header fields for output.
            // Some editors will put extra info in the image file, we only save the headers and the data.
            if(bmp_info_header.bit_count == 32) {
                bmp_info_header.size = sizeof(BMPInfoHeader) + sizeof(BMPColorHeader);
                file_header.offset_data = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader) + sizeof(BMPColorHeader);
            } else {
                bmp_info_header.size = sizeof(BMPInfoHeader);
                file_header.offset_data = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader);
            }
            file_header.file_size = file_header.offset_data;

            if (bmp_info_header.height < 0) {
                throw runtime_error("The program can treat only BMP images with the origin in the bottom left corner!");
            }

            data.resize(bmp_info_header.width * bmp_info_header.height * bmp_info_header.bit_count / 8);

            // Here we check if we need to take into account row padding
            if (bmp_info_header.width % 4 == 0) {
                inp.read((char*)data.data(), data.size());
                file_header.file_size += static_cast<uint32_t>(data.size());
            }
            else {
                row_stride = bmp_info_header.width * bmp_info_header.bit_count / 8;
                uint32_t new_stride = make_stride_aligned(4);
                vector<uint8_t> padding_row(new_stride - row_stride);

                for (int y = 0; y < bmp_info_header.height; ++y) {
                    inp.read((char*)(data.data() + row_stride * y), row_stride);
                    inp.read((char*)padding_row.data(), padding_row.size());
                }
                file_header.file_size += static_cast<uint32_t>(data.size()) + bmp_info_header.height * static_cast<uint32_t>(padding_row.size());
            }
            cout << "IMAGEM lida com sucesso" << endl;
        }
        else {
            throw runtime_error("Não consegui abrir a IMAGEM.");
        }
    }

    BMP(string image_name, int32_t width, int32_t height, bool has_alpha = true): image_name(image_name) {
        if (width <= 0 || height <= 0) {
            throw runtime_error("A largura e a altura da IMAGEM devem ser positiva.");
        }

        bmp_info_header.width = width;
        bmp_info_header.height = height;
        if (has_alpha) {
            bmp_info_header.size = sizeof(BMPInfoHeader) + sizeof(BMPColorHeader);
            file_header.offset_data = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader) + sizeof(BMPColorHeader);

            bmp_info_header.bit_count = 32;
            bmp_info_header.compression = 3;
            row_stride = width * 4;
            data.resize(row_stride * height);
            file_header.file_size = file_header.offset_data + data.size();
        }
        else {
            bmp_info_header.size = sizeof(BMPInfoHeader);
            file_header.offset_data = sizeof(BMPFileHeader) + sizeof(BMPInfoHeader);

            bmp_info_header.bit_count = 24;
            bmp_info_header.compression = 0;
            row_stride = width * 3;
            data.resize(row_stride * height);

            uint32_t new_stride = make_stride_aligned(4);
            file_header.file_size = file_header.offset_data + static_cast<uint32_t>(data.size()) + bmp_info_header.height * (new_stride - row_stride);
        }
    }

    void write() {
        ofstream of{ image_name.c_str(), ios_base::binary };
        if (of) {
            if (bmp_info_header.bit_count == 32) {
                write_headers_and_data(of);
            }
            else if (bmp_info_header.bit_count == 24) {
                if (bmp_info_header.width % 4 == 0) {
                    write_headers_and_data(of);
                }
                else {
                    uint32_t new_stride = make_stride_aligned(4);
                    vector<uint8_t> padding_row(new_stride - row_stride);

                    write_headers(of);

                    for (int y = 0; y < bmp_info_header.height; ++y) {
                        of.write((const char*)(data.data() + row_stride * y), row_stride);
                        of.write((const char*)padding_row.data(), padding_row.size());
                    }
                }
            }
            else {
                throw runtime_error("The program can treat only 24 or 32 bits per pixel BMP files");
            }
        }
        else {
            throw runtime_error("Unable to open the output image file.");
        }
        cout << "IMAGEM salva com sucesso" << endl;
    }

private:
    uint32_t row_stride{ 0 };

    void write_headers(ofstream &of) {
        of.write((const char*)&file_header, sizeof(file_header));
        of.write((const char*)&bmp_info_header, sizeof(bmp_info_header));
        if(bmp_info_header.bit_count == 32) {
            of.write((const char*)&bmp_color_header, sizeof(bmp_color_header));
        }
    }

    void write_headers_and_data(ofstream &of) {
        write_headers(of);
        of.write((const char*)data.data(), data.size());
    }

    // Add 1 to the row_stride until it is divisible with align_stride
    uint32_t make_stride_aligned(uint32_t align_stride) {
        uint32_t new_stride = row_stride;
        while (new_stride % align_stride != 0) {
            new_stride++;
        }
        return new_stride;
    }

    // Check if the pixel data is stored as BGRA and if the color space type is sRGB
    void check_color_header(BMPColorHeader &bmp_color_header) {
        BMPColorHeader expected_color_header;
        if(expected_color_header.red_mask != bmp_color_header.red_mask ||
            expected_color_header.blue_mask != bmp_color_header.blue_mask ||
            expected_color_header.green_mask != bmp_color_header.green_mask ||
            expected_color_header.alpha_mask != bmp_color_header.alpha_mask) {
            throw runtime_error("Unexpected color mask format! The program expects the pixel data to be in the BGRA format");
        }
        if(expected_color_header.color_space_type != bmp_color_header.color_space_type) {
            throw runtime_error("Unexpected color space type! The program expects sRGB values");
        }
    }
};

inline
cudaError_t checkCuda(cudaError_t result)
{
#if defined(DEBUG) || defined(_DEBUG)
  if (result != cudaSuccess) {
    fprintf(stderr, "CUDA Runtime Error: %s\n", cudaGetErrorString(result));
    assert(result == cudaSuccess);
  }
#endif
  return result;
}

__global__
void convolution2DKernel(const uint8_t *input, const float *kernel, uint8_t *output,
                          int inputWidth, int inputHeight,
                          int kernelWidth, int kernelHeight) {
    int col = blockIdx.x * blockDim.x + threadIdx.x;
    int row = blockIdx.y * blockDim.y + threadIdx.y;

    if (col < inputWidth && row < inputHeight) {
        int halfKernelWidth = kernelWidth / 2;
        int halfKernelHeight = kernelHeight / 2;

        float red_result = 0.0f;
        float green_result = 0.0f;
        float blue_result = 0.0f;

        for (int i = 0; i < kernelHeight; ++i) {
            for (int j = 0; j < kernelWidth; ++j) {
                int inputRow = row - halfKernelHeight + i;
                int inputCol = col - halfKernelWidth + j;

                if (inputRow >= 0 && inputRow < inputHeight && inputCol >= 0 && inputCol < inputWidth) {
                    float kernelValue = kernel[i * kernelWidth + j];
                    uint8_t blue = input[(inputRow * inputWidth + inputCol) * 3 + 0];
                    uint8_t green = input[(inputRow * inputWidth + inputCol) * 3 + 1];
                    uint8_t red = input[(inputRow * inputWidth + inputCol) * 3 + 2];

                    // Soma os resultados da convolução
                    red_result += kernelValue * (float) red;
                    green_result += kernelValue * (float) green;
                    blue_result += kernelValue * (float) blue;
                }
            }
        }

        // Atualiza o pixel na imagem de saída, considerando o tipo de dado
        output[(row * inputWidth + col) * 3 + 0] = (uint8_t) min(max(blue_result, 0.0f), 255.0f);
        output[(row * inputWidth + col) * 3 + 1] = (uint8_t) min(max(green_result, 0.0f), 255.0f);
        output[(row * inputWidth + col) * 3 + 2] = (uint8_t) min(max(red_result, 0.0f), 255.0f);
    }
}

int main() {
    string inputImage = "drive/MyDrive/convolucao/imagem474.bmp";
    string outputImage = "saida_convolucao.bmp";
    string kernelImage = "drive/MyDrive/convolucao/kernel_blur.txt";

    int DIVIDER = 255.0;

    // Read an image from disk, modify it and write it back:
    BMP bmp(inputImage);

    // Lê o kernel de convolução a partir de um arquivo de texto
    ifstream kernelFile(kernelImage);
    if (!kernelFile.is_open()) {
        cerr << "Erro ao abrir o arquivo de kernel." << endl;
        return 1;
    }

    vector<float> kernel;
    float value;
    while (kernelFile >> value) {
        kernel.push_back(value / DIVIDER);
    }

    kernelFile.close();

    int kernelWidth = static_cast<int>(sqrt(kernel.size()));
    int kernelHeight = kernelWidth;

    int inputWidth = bmp.bmp_info_header.width;
    int inputHeight = bmp.bmp_info_header.height;

    BMP novaImagem = BMP(outputImage, bmp.bmp_info_header.width, bmp.bmp_info_header.height, false);

    uint8_t *d_input, *d_output;
    float *d_kernel;
    checkCuda(cudaMalloc((void **)&d_input, bmp.data.size() * sizeof(uint8_t)));
    checkCuda(cudaMalloc((void **)&d_kernel, kernel.size() * sizeof(float)));
    checkCuda(cudaMalloc((void **)&d_output, novaImagem.data.size() * sizeof(uint8_t)));

    checkCuda(cudaMemcpy(d_input, bmp.data.data(), bmp.data.size() * sizeof(uint8_t), cudaMemcpyHostToDevice));
    checkCuda(cudaMemcpy(d_kernel, kernel.data(), kernel.size() * sizeof(float), cudaMemcpyHostToDevice));

    dim3 blockSize(16, 16);
    dim3 gridSize((inputWidth + blockSize.x - 1) / blockSize.x, (inputHeight + blockSize.y - 1) / blockSize.y);

    convolution2DKernel<<<gridSize, blockSize>>>(d_input, d_kernel, d_output,
                                                 inputWidth, inputHeight,
                                                 kernelWidth, kernelHeight);

    checkCuda(cudaMemcpy(novaImagem.data.data(), d_output, novaImagem.data.size() * sizeof(uint8_t), cudaMemcpyDeviceToHost));

    novaImagem.write();

    checkCuda(cudaFree(d_input));
    checkCuda(cudaFree(d_kernel));
    checkCuda(cudaFree(d_output));

    return 0;
}