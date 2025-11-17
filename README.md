
# Axiom Trade WebSocket Filter

Un filtro limpio y estructurado para mensajes de WebSocket y respuestas HTTP de Axiom Trade usando mitmproxy.

## 📋 Descripción

Este proyecto filtra mensajes de WebSocket y respuestas XHR de axiom.trade basándose en criterios configurables como direcciones de wallet de desarrolladores y direcciones de financiamiento.

## 🏗️ Estructura del Proyecto

```
axiomfilter/
├── axiom_filter.py      # Addon principal de mitmproxy
├── config.py            # Configuración y direcciones de wallet
├── filters.py           # Lógica de filtrado
├── models.py            # Modelos de datos
├── example.py           # Código anterior (referencia)
├── new_pairs.json       # Ejemplo de mensaje new_pairs
├── update_pulse.json    # Ejemplo de mensaje update_pulse_v2
└── xhr.json             # Ejemplo de respuesta /pulse
```

## ✨ Características

- **Filtrado de WebSocket**: Filtra mensajes del room `update_pulse_v2` basándose en criterios
- **Filtrado de XHR**: Filtra respuestas del endpoint `/pulse`
- **Configurable**: Fácil configuración de direcciones y criterios
- **Estadísticas**: Muestra estadísticas de filtrado al finalizar
- **Código limpio**: Organizado en módulos separados con responsabilidades claras

## 🔧 Requisitos

```bash
pip install mitmproxy
```

## 🚀 Uso

### Uso Básico

```bash
# Ejecutar con la configuración por defecto
mitmdump -s axiom_filter.py

# Con interfaz web
mitmweb -s axiom_filter.py

# Con interfaz de terminal
mitmproxy -s axiom_filter.py
```

### Configuración

Edita `config.py` para personalizar los filtros:

```python
from config import config

# Agregar una dirección de desarrollador
config.add_dev_address("TU_DIRECCION_AQUI")

# Agregar una dirección de financiamiento
config.add_funder_address("TU_DIRECCION_AQUI")

# Habilitar/deshabilitar filtros
config.FILTER_BY_DEV_ADDRESS = True
config.FILTER_BY_FUNDING_WALLET = True

# Habilitar logging detallado
config.VERBOSE_LOGGING = True
```

### Ejemplo Avanzado

Crear un script personalizado:

```python
# custom_filter.py
from axiom_filter import AxiomTradeFilter
from config import FilterConfig

# Crear configuración personalizada
custom_config = FilterConfig()
custom_config.FUNDER_ADDRESSES = {
    "5jYaYv7HoiFVrY9bAcruj6dH8fCBseky4sBmnTFGSaeW",
    "OTRA_DIRECCION_AQUI"
}
custom_config.FILTER_BY_FUNDING_WALLET = True
custom_config.VERBOSE_LOGGING = True

# Crear addon con configuración personalizada
addons = [AxiomTradeFilter(custom_config)]
```

Ejecutar:
```bash
mitmdump -s custom_filter.py
```

## 📊 Tipos de Mensajes

### 1. Update Pulse (WebSocket)

Mensajes del room `update_pulse_v2` que contienen arrays con información de tokens.

**Criterios de filtrado:**
- Dirección del desarrollador (índice 2)
- Información de financiamiento de wallet (índice 39)

### 2. New Pairs (WebSocket)

Mensajes del room `new_pairs` con información de nuevos pares de tokens.

**Por defecto:** Mantiene todos los mensajes (personalizable en `filters.py`)

### 3. XHR /pulse

Respuestas HTTP del endpoint `/pulse` con información de tokens.

**Criterios de filtrado:**
- `devAddress`
- `devWalletFunding.fundingWalletAddress`

## 🎯 Filtros Disponibles

### Filtro por Dirección de Desarrollador
```python
config.FILTER_BY_DEV_ADDRESS = True
config.DEV_ADDRESSES = {
    "54bV9JqbBYH5hVCXe41mkdSioPPBZULCrJYfHVfagnME",
    "6muPgMoshvTJQzJ3EteaGLxpz5ZTDYHZ5HzMQCNiZ4hh",
}
```

### Filtro por Wallet de Financiamiento
```python
config.FILTER_BY_FUNDING_WALLET = True
config.FUNDER_ADDRESSES = {
    "5jYaYv7HoiFVrY9bAcruj6dH8fCBseky4sBmnTFGSaeW",
}
```

## 📈 Estadísticas

Al finalizar, el filtro muestra estadísticas:

```
=== Filter Statistics ===
Update Pulse: 15/100 items kept
XHR Responses: 5/20 items kept
New Pairs: 10/10 messages kept
```

## 🔍 Logging

El sistema incluye dos niveles de logging:

- **ENABLE_LOGGING**: Muestra información general
- **VERBOSE_LOGGING**: Muestra información detallada de cada mensaje

## 📝 Modelos de Datos

### UpdatePulseItem
Representa un item del array `update_pulse_v2` con 43+ campos incluyendo:
- Direcciones (pair, token, dev)
- Información del token
- Métricas de holders y trading
- Información de financiamiento

### XHRPulseResponse
Representa la respuesta del endpoint `/pulse` con campos en formato camelCase.

### DevWalletFunding
Información de financiamiento de wallet del desarrollador.

## 🛠️ Personalización

### Agregar Filtros Personalizados para New Pairs

Edita el método `should_keep_new_pair` en `filters.py`:

```python
def should_keep_new_pair(self, content: Dict[str, Any]) -> bool:
    # Filtrar por protocolo
    if content.get("protocol") == "Pump V1":
        return True
    
    # Filtrar por liquidez inicial
    if content.get("initial_liquidity_sol", 0) > 50:
        return True
    
    return False
```

### Agregar Filtros Adicionales para Update Pulse

Edita el método `should_keep_update_pulse_item` en `filters.py`:

```python
def should_keep_update_pulse_item(self, item_array: List[Any]) -> bool:
    item = UpdatePulseItem.from_array(item_array)
    
    # Filtro por market cap
    if item.market_cap_sol > 1000:
        return True
    
    # Filtro por número de holders
    if item.num_holders > 100:
        return True
    
    # Filtros existentes...
    return False
```

## 🔗 Conexión con Navegador

### Chrome/Chromium
```bash
chromium --proxy-server="localhost:8080" --ignore-certificate-errors
```

### Firefox
Configurar en Settings → Network Settings → Manual proxy configuration:
- HTTP Proxy: localhost
- Port: 8080
- Use this proxy for HTTPS

### Instalar Certificado de mitmproxy
```bash
# El certificado se genera automáticamente
# Visita http://mitm.it para descargarlo
```

## 🐛 Debug

Para ver todos los mensajes sin filtrar:

```python
config.FILTER_BY_DEV_ADDRESS = False
config.FILTER_BY_FUNDING_WALLET = False
config.VERBOSE_LOGGING = True
```

## 📦 Dependencias

- Python 3.7+
- mitmproxy

## 🤝 Contribuir

El código está estructurado para facilitar extensiones:

1. **config.py**: Agregar nuevas configuraciones
2. **models.py**: Agregar nuevos modelos de datos
3. **filters.py**: Agregar nueva lógica de filtrado
4. **axiom_filter.py**: Agregar nuevos hooks de mitmproxy

## 📄 Licencia

Este proyecto es para uso personal y educativo.

## ⚠️ Notas

- Los índices del array `update_pulse_v2` están documentados en `models.py`
- El filtro mantiene compatibilidad con el formato actual de axiom.trade
- Los mensajes que no pasan los filtros son eliminados (dropped)
- Las respuestas XHR filtradas devuelven arrays vacíos o objetos vacíos

## 🔄 Diferencias con example.py

- **Código organizado** en múltiples archivos con responsabilidades claras
- **Modelos de datos** tipados con dataclasses
- **Configuración centralizada** fácil de modificar
- **Estadísticas** de filtrado
- **Mejor logging** con niveles configurables
- **Fácil de extender** con nueva funcionalidad
