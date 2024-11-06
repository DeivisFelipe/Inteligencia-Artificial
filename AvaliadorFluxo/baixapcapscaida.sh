# URL = https://data.caida.org/datasets/passive-2019
# Descrição: Baixa os arquivos pcap de 2019 da CAIDA

url="https://data.caida.org/datasets/passive-2019/equinix-nyc/20190117-130000.UTC/"
user=""
password=""

# Deleta o index.html
rm index.html

# Acessa a página com os arquivos pcap e loga
wget --user="$user" --password="$password" "$url"

# Le o arquivo index.html e pega todos as tags <a> que contem o nome do arquivo pcap
grep -oP '(?<=href=")[^"]*' index.html | grep pcap.gz > arquivos.txt

# Verifica se a pasta pcaps existe, se não, cria
if [ ! -d pcaps ]; then
    mkdir pcaps
fi

# Baixa os arquivos pcap
skip=2
count=0
reads_lines=13

while read line; do
    # Incrementa o contador de linhas
    count=$((count + 1))

    if [ $count -gt $skip ] && [ $count -le $((skip + reads_lines)) ]; then

        # Verifica se o arquivo já foi baixado e está na pasta pcaps
        if [ -f pcaps/$line ]; then
            echo "Arquivo $line já baixado"
        else
            echo "Baixando $line"
            wget --user="$user" --password="$password" -P pcaps "$url$line"
        fi
    fi

    if [ $count -gt $((skip + reads_lines)) ]; then
        break
    fi
done < arquivos.txt

