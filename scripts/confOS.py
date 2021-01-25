#!/usr/bin/env python3
import os
import subprocess
import sys
import stdiomask
import json
from urllib import request

def compruebaSistema():
  platform = sys.platform
  return platform
  
def obtenerUSERHOME():
  USER=subprocess.check_output('echo $(logname)', shell=True).decode('utf-8').rstrip("\n")
  HOME=os.path.expanduser('~'+USER)
  return USER,HOME

def crearDirectorio(user, directorio):

  existeDir = os.path.exists(directorio)

  if (not existeDir):
    os.system('runuser -l ' + user + ' -c \"mkdir ' + directorio + "\"")
    existeDir = os.path.exists(directorio)
    if (existeDir):
      print('Se ha creado correctamente el directorio ' + directorio)
      
def instalarProgramas(listaProgramasToInstall,listaProgramasAPT,listaProgramasSNAP):
  
  if not listaProgramasToInstall:
    os.system('apt-get update')
  
  for programa in listaProgramasToInstall:
    if programa in listaProgramasAPT:
        os.system('apt-get install ' + programa + ' -y')
    
    if programa in listaProgramasSNAP:
        os.system('snap install ' + programa + ' --classic --edge')

def obtenerReposGitHub(gitUser,gitToken=""):
  if (gitUser != ""):
    if ((gitToken != "") and (len(gitToken) > 10)):

      url = "https://api.github.com/user/repos?access_token=" + gitToken
    
    else:
  
      url = "https://api.github.com/users/" + gitUser + "/repos"
  
    r = request.Request(url)
    response = request.urlopen(r)
    data=response.read().decode('utf-8')
    lista=[]
    lista=data.split(",")
    listaRepos=[]
    for dato in lista:
      if "\"name\":" in dato:
        dato="{" + dato + "}"
        dato=json.loads(dato)
        listaRepos.append(dato['name'])
      
    print(listaRepos)
  
    return listaRepos

def clonarRepositorios(gitUser="",gitPassword="",gitToken="",listaRepos="",listaReposToDownload=""):

  if (not gitUser == ""):
    user,home=obtenerUSERHOME()
    ruta = home + '/Desarrollo'
    crearDirectorio(user,ruta)

    for repositorio in listaReposToDownload:
      if repositorio in listaRepos:
        os.system('runuser -l ' + user + ' -c \"cd ' + ruta + ' && git clone http://' + gitUser + ':' + gitPassword + '@github.com/' + gitUser + '/' + repositorio + '.git\"')

def askPrograms():
  listaProgramasAPT = ['git','libreoffice','arduino','snapd','libqt5designer5','sequeler','spectator','simplenote','conky-all']
  listaProgramasSNAP = ['intellij-idea-community','android-studio','joplin-james-carroll']
  listaProgramasToShow=[]
  listaProgramasToInstall=[]
  listaProgramasToShow.extend(listaProgramasAPT)
  listaProgramasToShow.extend(listaProgramasSNAP)
  
  print('\n--------------------')
  print('PROGRAMAS A INSTALAR')
  print('--------------------')
  print()
  print(listaProgramasToShow)
  
  programas=input('¿Qué programas quieres instalar? Escribe \'*\' para instalar todos (Separados por comas): ')
   
  if '*' in programas:
    listaProgramasToInstall=listaProgramasToShow
  
  else:
    listaProgramasToInstall=programas.split(',')
   
  return listaProgramasToInstall,listaProgramasAPT,listaProgramasSNAP

def askGitHub():
  print('\n-------------------')
  print('CLONAR REPOSITORIOS')
  print('-------------------')
  gitUser=input('\nUsuario de GitHub: ')
  gitPassword=stdiomask.getpass(prompt='Contraseña de GitHub: ')
  gitToken=stdiomask.getpass(prompt='Token de GitHub (necesario para consultar repositorios privados): ')
  listaRepos=obtenerReposGitHub(gitUser,gitToken)
  repos=input('\n¿Qué repositorios desea clonar? \"*\" para descargar todos (Separados por comas): ')
  
  listaReposToDownload=[]
  
  if repos == "*":
    listaReposToDownload=listaRepos
  elif (listaReposToDownload != "*"):
    listaReposToDownload=repos.split(",")
    
  return gitUser,gitPassword,gitToken,listaRepos,listaReposToDownload
  
def backUpRSync(rutaOrigen,rutaDestino):

  os.system('rsync -av --update ' + rutaOrigen + " " + rutaDestino)

def configuracionInicial():
  
  print('\n---------------------------------------------')
  print('INICIANDO EL PROCESO DE CONFIGURACION INICIAL')
  print('---------------------------------------------')
  
  gitUser=""
  gitPassword=""
  gitToken=""
  listaRepos=[]
  listaReposToDownload=[]
  
  listaProgramasToInstall,listaProgramasAPT,listaProgramasSNAP=askPrograms()
  
  configGit = input('\n¿Desea descargar sus repositorios de GitHub? s/N: ')

  if (configGit.lower() == 's'):
    gitUser,gitPassword,gitToken,listaRepos,listaReposToDownload=askGitHub()
  else:
    pass
  
  instalarProgramas(listaProgramasToInstall,listaProgramasAPT,listaProgramasSNAP)
  clonarRepositorios(gitUser,gitPassword,gitToken,listaRepos,listaReposToDownload)
  
  print('\nEl proceso de configuracion inicial ha terminado correctamente')

##INICIO DEL PROGRAMA
sistemaOperativo = compruebaSistema()

valor=""

while (valor!="0"):
    print('\nPrograma de configuracion de devpefer v0.1')
    print('Sistema operativo: ' + sistemaOperativo[0:1].upper()+sistemaOperativo[1:])

    if(sistemaOperativo == 'linux'):
      print('\n0) Salir')
      print('\n1) Configuracion inicial')
      print('\n2) Instalar programas')
      print('\n3) Clonar repositorios')
      print('\n4) BackUp con RSync')
      
      valor = input("\nElige una opcion: ")

      if (valor == "1"):
        
        configuracionInicial()

      elif (valor == "2"):

        listaProgramsToDownload,listaProgramsAPT,listaProgramsSNAP=askPrograms()
        instalarProgramas(listaProgramsToDownload,listaProgramsAPT,listaProgramsSNAP)
        
      elif (valor == "3"):
        gitUser,gitPassword,gitToken,listaRepos,listaReposToDownload=askGitHub()
        clonarRepositorios(gitUser,gitPassword,gitToken,listaRepos,listaReposToDownload)
        
      elif (valor == "4"):
      
          rutaOrigen=input('Ruta origen: ')
          rutaDestino=input('Ruta destino: ')
          
          backUpRSync(rutaOrigen,rutaDestino)
