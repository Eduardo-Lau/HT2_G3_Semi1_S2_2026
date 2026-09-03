#!/usr/bin/env python3
"""
Script de verificación para validar el correcto funcionamiento de las APIs
según los requerimientos de la Hoja de Trabajo 2 - Seminario de Sistemas 1.

Uso:
    python test_apis.py [url_api1] [url_api2]
Ejemplo local:
    python test_apis.py http://localhost:3000 http://localhost:5000
Ejemplo en Azure / Balanceador:
    python test_apis.py http://<IP_VM1>:3000 http://<IP_VM2>:3000
    python test_apis.py http://<DNS_O_IP_BALANCEADOR>
"""

import sys
import json
import urllib.request
import urllib.error

# Configurar encoding seguro para Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def test_endpoint(base_url, endpoint):
    url = f"{base_url.rstrip('/')}{endpoint}"
    print(f"\nProbando: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'HT2-Tester/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            body_raw = response.read().decode('utf-8')
            print(f"  [+] Codigo HTTP: {status_code}")
            
            if endpoint == '/check':
                if status_code == 200:
                    print("  [OK] /check respondio exitosamente con HTTP 200")
                    return True
                else:
                    print(f"  [ERROR] Se esperaba 200, recibido: {status_code}")
                    return False
            
            elif endpoint == '/info':
                try:
                    data = json.loads(body_raw)
                    print(f"  [OK] Respuesta JSON recibida:\n{json.dumps(data, indent=4, ensure_ascii=False)}")
                    required_keys = ["Instancia", "Curso", "Grupo"]
                    missing = [k for k in required_keys if k not in data]
                    if not missing:
                        print("  [OK] Estructura JSON valida (contiene 'Instancia', 'Curso', 'Grupo')")
                        return True
                    else:
                        print(f"  [ERROR] Faltan claves en el JSON: {missing}")
                        return False
                except json.JSONDecodeError:
                    print(f"  [ERROR] La respuesta no es un JSON valido: {body_raw}")
                    return False
                    
    except urllib.error.HTTPError as e:
        print(f"  [ERROR] Error HTTP {e.code}: {e.reason}")
        return False
    except urllib.error.URLError as e:
        print(f"  [ERROR] Error de conexion: {e.reason}")
        return False
    except Exception as e:
        print(f"  [ERROR] Excepcion inesperada: {e}")
        return False

def main():
    args = sys.argv[1:]
    urls = args if args else ["http://localhost:3000", "http://localhost:5000"]
    
    total_passed = 0
    total_tests = 0
    
    print("=" * 60)
    print(" Verificacion de Endpoints - Hoja de Trabajo 2")
    print("=" * 60)
    
    for i, base_url in enumerate(urls, 1):
        print(f"\n>>> Verificando Servicio {i}: {base_url}")
        for ep in ['/check', '/info']:
            total_tests += 1
            if test_endpoint(base_url, ep):
                total_passed += 1
                
    print("\n" + "=" * 60)
    print(f" Resultado final: {total_passed}/{total_tests} pruebas exitosas.")
    print("=" * 60)
    
    if total_passed == total_tests:
        print("[EXITO] Todos los endpoints cumplen con la especificacion!")
        sys.exit(0)
    else:
        print("[ALERTA] Algunas pruebas fallaron. Revisa los mensajes anteriores.")
        sys.exit(1)

if __name__ == '__main__':
    main()
