-- Script de inicialização do banco de dados MySQL
-- Criação da tabela para armazenar dados de contas a receber do XML

USE contas_receber;

-- Tabela principal de contas a receber
CREATE TABLE IF NOT EXISTS contas_receber (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tipopessoa CHAR(1) NOT NULL COMMENT 'F=Física, J=Jurídica',
    codcliente INT NOT NULL,
    cpf VARCHAR(14) NULL COMMENT 'CPF ou CNPJ formatado',
    nome VARCHAR(255) NOT NULL,
    fksiglalogra VARCHAR(10) NULL COMMENT 'Tipo de logradouro (RUA, AV, etc)',
    logradouro VARCHAR(255) NULL,
    numero VARCHAR(20) NULL,
    bairro VARCHAR(100) NULL,
    cep VARCHAR(8) NULL,
    descmuni VARCHAR(100) NULL COMMENT 'Nome do município',
    uf CHAR(2) NULL,
    codoper INT NULL,
    descoper VARCHAR(255) NULL COMMENT 'Descrição da operação',
    nfserie VARCHAR(10) NULL,
    nfnum VARCHAR(20) NULL,
    valtotalnf DECIMAL(15,2) NULL COMMENT 'Valor total da nota fiscal',
    numerocontrato VARCHAR(50) NULL,
    nossonumero VARCHAR(50) NULL COMMENT 'Nosso número do boleto',
    numeroparcela INT NULL,
    datacontrato DATE NULL,
    datavencimento DATE NOT NULL,
    valordocumento DECIMAL(15,2) NOT NULL,
    codigoformapagto INT NULL,
    descricaoformapagto VARCHAR(100) NULL,
    vendcod INT NULL COMMENT 'Código do vendedor',
    nomevend VARCHAR(255) NULL,
    codmov BIGINT NULL,
    statusdoc VARCHAR(50) NULL COMMENT 'Status do documento (ex: 0-ABERTO)',
    rg VARCHAR(20) NULL,
    datanascimento DATE NULL,
    fone VARCHAR(20) NULL COMMENT 'Telefone/WhatsApp',
    email VARCHAR(255) NULL COMMENT 'Email do cliente (pode ser preenchido posteriormente)',
    email_enviado BOOLEAN DEFAULT FALSE COMMENT 'Flag para controle de envio de email',
    whatsapp_enviado BOOLEAN DEFAULT FALSE COMMENT 'Flag para controle de envio WhatsApp',
    data_envio_email DATETIME NULL,
    data_envio_whatsapp DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_codcliente (codcliente),
    INDEX idx_cpf (cpf),
    INDEX idx_datavencimento (datavencimento),
    INDEX idx_nossonumero (nossonumero),
    INDEX idx_numerocontrato (numerocontrato),
    INDEX idx_statusdoc (statusdoc),
    INDEX idx_email_enviado (email_enviado),
    INDEX idx_whatsapp_enviado (whatsapp_enviado),
    INDEX idx_datavencimento_status (datavencimento, statusdoc)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Tabela para armazenar contas a receber importadas do XML';

-- Tabela para histórico de envios (logs de envios de email e WhatsApp)
CREATE TABLE IF NOT EXISTS historico_envios (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    conta_receber_id BIGINT NOT NULL,
    tipo_envio ENUM('email', 'whatsapp') NOT NULL,
    destinatario VARCHAR(255) NOT NULL COMMENT 'Email ou número de telefone',
    status ENUM('enviado', 'falhou', 'pendente') NOT NULL DEFAULT 'pendente',
    mensagem_erro TEXT NULL,
    data_envio DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conta_receber_id) REFERENCES contas_receber(id) ON DELETE CASCADE,
    INDEX idx_conta_receber_id (conta_receber_id),
    INDEX idx_tipo_envio (tipo_envio),
    INDEX idx_status (status),
    INDEX idx_data_envio (data_envio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Histórico de envios de emails e WhatsApp';

-- Tabela para configurações do sistema
CREATE TABLE IF NOT EXISTS configuracao_sistema (
    id INT AUTO_INCREMENT PRIMARY KEY,
    chave VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT NULL,
    descricao VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Configurações gerais do sistema';

-- Inserir algumas configurações padrão
INSERT INTO configuracao_sistema (chave, valor, descricao) VALUES
    ('dias_antes_vencimento', '3,1', 'Dias antes do vencimento para enviar lembretes'),
    ('email_habilitado', 'true', 'Habilita envio de emails'),
    ('whatsapp_habilitado', 'true', 'Habilita envio de WhatsApp')
ON DUPLICATE KEY UPDATE valor=valor;

