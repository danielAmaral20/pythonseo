import streamlit as st
import requests
import pandas as pd

def check_https_status(url):
    try:
        response = requests.head(url, timeout=5)
        status_code = response.status_code
        status_description = get_status_description(status_code)
        return status_code, status_description
    except requests.exceptions.RequestException:
        return "Erro de conexão", ""

def get_status_description(status_code):
    status_codes = {
        100: "Continue - O cliente deve continuar a solicitação ou ignorar a resposta se a solicitação já estiver concluída.",
        101: "Switching Protocols - O servidor está mudando para um protocolo diferente.",
        102: "Processing (WebDAV) - O servidor recebeu e está processando a requisição, mas nenhuma resposta está disponível ainda.",
        103: "Early Hints Experimental - O servidor está preparando uma resposta enquanto o agente do usuário inicia o pré-carregamento de recursos.",
        200: "OK - A solicitação foi bem-sucedida.",
        201: "Created - O recurso foi criado como resultado da requisição.",
        202: "Accepted - A requisição foi recebida, mas ainda não foi atendida.",
        203: "Non-Authoritative Information - Os metadados retornados não são exatamente os mesmos disponíveis no servidor de origem.",
        204: "No Content - Não há conteúdo para enviar para esta solicitação.",
        205: "Reset Content - O agente do usuário deve redefinir o documento que enviou esta solicitação.",
        206: "Partial Content - A resposta contém apenas parte do recurso solicitado.",
        207: "Multi-Status (WebDAV) - Transmite informações sobre vários recursos.",
        208: "Already Reported (WebDAV) - Usado para evitar enumerar repetidamente membros internos de várias ligações para a mesma coleção.",
        226: "IM Used (HTTP Delta encoding) - O servidor atendeu a uma solicitação GET para o recurso.",
        300: "Multiple Choices - A solicitação tem mais de uma resposta possível.",
        301: "Moved Permanently - O URL do recurso solicitado foi alterado permanentemente.",
        302: "Found - O URI do recurso solicitado foi alterado temporariamente.",
        303: "See Other - O cliente deve obter o recurso solicitado em outro URI com uma solicitação GET.",
        304: "Not Modified - Indica que a resposta não foi modificada.",
        305: "Use Proxy Deprecated - Este código foi descontinuado devido a questões de segurança.",
        306: "Unused Deprecated - Este código de resposta não é mais usado.",
        307: "Temporary Redirect - O cliente deve obter o recurso solicitado em outra URI com o mesmo método usado na solicitação anterior.",
        308: "Permanent Redirect - O recurso está permanentemente localizado em outro URI.",
        400: "Bad Request - O servidor não pode ou não irá processar a solicitação devido a um erro do cliente.",
        401: "Unauthorized - O cliente deve se autenticar para obter a resposta solicitada.",
        402: "Payment Required Experimental - Reservado para uso futuro.",
        403: "Forbidden - O cliente não tem direitos de acesso ao conteúdo.",
        404: "Not Found - O servidor não pode encontrar o recurso solicitado.",
        405: "Method Not Allowed - O método de solicitação não é suportado pelo servidor.",
        406: "Not Acceptable - O servidor não pode fornecer conteúdo que seja aceitável para o agente do usuário.",
        407: "Proxy Authentication Required - A autenticação é necessária para acessar o proxy.",
        408: "Request Timeout - O servidor encerrou a conexão devido a uma solicitação ociosa.",
        409: "Conflict - A solicitação conflita com o estado atual do servidor.",
        410: "Gone - O recurso solicitado foi excluído permanentemente.",
        411: "Length Required - O servidor rejeitou a solicitação porque o campo de cabeçalho Content-Length não está definido.",
        412: "Precondition Failed - O cliente indicou pré-condições que o servidor não atende.",
        413: "Payload Too Large - A entidade da solicitação é maior do que os limites definidos pelo servidor.",
        414: "URI Too Long - O URI solicitado é mais longo do que o servidor está disposto a interpretar.",
        415: "Unsupported Media Type - O formato de mídia dos dados da solicitação não é suportado pelo servidor.",
        416: "Range Not Satisfiable - O intervalo especificado na solicitação não pode ser atendido.",
        417: "Expectation Failed - O servidor não pode atender às expectativas indicadas pelo campo de cabeçalho Expect.",
        418: "I'm a teapot - O servidor recusa a tentativa de coar café num bule de chá.",
        421: "Misdirected Request - A requisição foi direcionada a um servidor inapto a produzir a resposta.",
        422: "Unprocessable Content (WebDAV) - A solicitação foi bem formada, mas não pôde ser atendida devido a erros semânticos.",
        423: "Locked (WebDAV) - O recurso está bloqueado.",
        424: "Failed Dependency (WebDAV) - A solicitação falhou devido à falha de uma solicitação anterior.",
        425: "Too Early Experimental - O servidor não está disposto a correr o risco de processar uma solicitação que pode ser repetida.",
        426: "Upgrade Required - O servidor se recusa a executar a solicitação usando o protocolo atual.",
        428: "Precondition Required - O servidor requer que a solicitação seja condicional.",
        429: "Too Many Requests - O usuário enviou muitas requisições num dado tempo.",
        431: "Request Header Fields Too Large - O servidor não está disposto a processar a solicitação devido a campos de cabeçalho muito grandes.",
        451: "Unavailable For Legal Reasons - O recurso solicitado não pode ser fornecido legalmente.",
        500: "Internal Server Error - O servidor encontrou uma situação com a qual não sabe lidar.",
        501: "Not Implemented - O servidor não suporta o método da requisição.",
        502: "Bad Gateway - O servidor obteve uma resposta inválida ao atuar como um gateway.",
        503: "Service Unavailable - O servidor não está pronto para manipular a requisição devido a sobrecarga ou manutenção.",
        504: "Gateway Timeout - O servidor, ao atuar como um gateway, não obteve uma resposta a tempo.",
        505: "HTTP Version Not Supported - A versão HTTP usada na requisição não é suportada pelo servidor.",
        506: "Variant Also Negotiates - O servidor tem um erro de configuração interna.",
        507: "Insufficient Storage (WebDAV) - O servidor não pode armazenar a representação necessária para concluir a solicitação.",
        508: "Loop Detected (WebDAV) - O servidor detectou um loop infinito ao processar a solicitação.",
        510: "Not Extended - Extensões adicionais à solicitação são necessárias.",
        511: "Network Authentication Required - O cliente precisa se autenticar para obter acesso à rede."
    }
    return status_codes.get(status_code, "Descrição não encontrada")

def main():
    st.title("Validador de status HTTPS")

    st.write("Este aplicativo verifica o status HTTPS de uma lista de URLs.")

    urls = st.text_area("Insira as URLs uma por linha")

    if st.button("Verificar"):
        urls_list = urls.split("\n")
        data = []
        for url in urls_list:
            if url.strip():
                status_code, status_description = check_https_status(url.strip())
                data.append({"URL": url, "Status Code": status_code, "Descrição": status_description})
        
        df = pd.DataFrame(data)
        st.write(df)

if __name__ == "__main__":
    main()
