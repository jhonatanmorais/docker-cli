
#!/usr/bin/env python3
import docker
import argparse
import sys
from datetime import datetime

def logando(mensagem, e, logfile="docker-cli.log"):
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open('docker-cli.log','a') as log:
        texto = "[%s] \t %s %s \n" % (data_atual, mensagem, str(e))
        log.write(texto)

def criar_container(args):
    try:
        client = docker.from_env()
        created = client.containers.run(args.imagem, args.comando)
        get_last_created =  client.containers.list(limit=1)
        for cada_container in get_last_created:
            new_container =  client.containers.get(cada_container.id)
            print("> Docker-CLI > NOVO CONTAINER > ID: %s | IMAGE: %s | COMMAND: %s | NAME: %s" % (new_container.short_id, new_container.attrs['Config']['Image'], new_container.attrs['Config']['Cmd'], new_container.name))
            return(new_container)
    except docker.errors.ImageNotFound as e:
        print("Erro: Imagem não existe.", e)
        logando("Erro: Imagem não existe.", e)
    except docker.errors.NotFound as e:
        print("Erro: Imagem não existe.", e)
        logando("Erro: Esse comando não existe.",e)
    except Exception as e:
        print("Erro: Ocorreu um erro inesperado.", e)
        logando("Erro: Ocorreu um erro inesperado.",e)

def listar_containers(args):
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)
        containers_list = []
        print("> Docker-CLI > LISTA DE CONTAINERS:\n")
        for cada_container in get_all:
            conectando =  client.containers.get(cada_container.id)
            print("> ID: %s | IMAGE: %s | COMMAND: %s | NAME: %s | STATUS: %s" % (conectando.short_id, conectando.attrs['Config']['Image'], conectando.attrs['Config']['Cmd'], conectando.name, conectando.status))
        return(get_all)
    except Exception as e:
        print("Erro: Ocorreu um erro inesperado.", e)
        logando("Erro: Ocorreu um erro inesperado.",e)

def procurar_container(args):
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)
        encontrados = []
        print("> Docker-CLI > CONTAINERS ENCONTRADOS POR IMAGEM: %s" % (args.imagem))
        for cada_container in get_all:
            conectando = client.containers.get(cada_container.id)
            imagem = conectando.attrs['Config']['Image']
            if str(args.imagem).lower() in str(imagem).lower():
                print("> ID: %s | IMAGE: %s | COMMAND: %s | NAME: %s | STATUS: %s" % (conectando.short_id, conectando.attrs['Config']['Image'], conectando.attrs['Config']['Cmd'], conectando.name, conectando.status))
                encontrados.append(conectando)
        if len(encontrados)<=0:
            print("Nenhum container encontrado.")
        return(encontrados)
    except Exception as e:
        print("Erro: Ocorreu um erro inesperado.", e)
        logando("Erro: Ocorreu um erro inesperado.", e)


def remover_container(args):
    try:
        client = docker.from_env()
        get_all = client.containers.list(all)
        print("> Docker-CLI > CONTAINERS REMOVIDOS:\n")
        removidos = []
        for cada_container in get_all:
            conectando = client.containers.get(cada_container.id)
            portas = conectando.attrs['HostConfig']['PortBindings']
            if isinstance(portas,dict):
                for porta, porta1 in portas.items():
                    porta1 = str(porta1)
                    porta2 = ''.join(filter(str.isdigit, porta1))
                    if int(porta2) <= 1024:
                        print("> Removido | ID: %s | PORT BINDING: %s | HOST PORT: %s" % (cada_container.id, porta, porta2))
                        removidos.append(conectando)
                        removendo = cada_container.remove(force=True)
        if len(removidos)<=0:
            print("Nenhum container foi removido.")
    except Exception as e:
        print("Erro: Ocorreu um erro inesperado.", e)
        logando("Erro: Ocorreu um erro inesperado.", e)


parser = argparse.ArgumentParser(description="Docker-CLI - Criado na aula de Python")
subparser = parser.add_subparsers()

criar_opt = subparser.add_parser('criar')
criar_opt.add_argument('--imagem', required=True, help='Nome da imagem')
criar_opt.add_argument('--comando', required=True, help='Comando a ser executado no container')
criar_opt.set_defaults(func=criar_container)

listar_opt = subparser.add_parser('listar')
listar_opt.set_defaults(func=listar_containers)

procurar_opt = subparser.add_parser('procurar')
procurar_opt.add_argument('--imagem', required=True, help='Nome da imagem')
procurar_opt.set_defaults(func=procurar_container)

remover_opt = subparser.add_parser('remover')
remover_opt.set_defaults(func=remover_container)

cmd = parser.parse_args()
cmd.func(cmd)