# Proyecto de fin de Master.
## Programa de fidelización que utiliza tokens ERC20.

Implementación del token **Puntos Recompensas Coin** utilizando el estandar [ERC-20](https://eips.ethereum.org/EIPS/eip-20), desarrollada en [Solidity](https://github.com/ethereum/solidity).

## Instalación

1. Descargar el repositorio 
   git clone ...

2. [Instalar Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), en el caso de que no este instalado.

## Uso

Para utilizar e interactuar localmente el contrato desplegado, se debe ejecutar en consola.  
 
```bash
brownie console
```

Siguiente, desplegar el token Puntos Recompensas Coin:

```python
>>> contrato = PuntosFidelizacion.deploy({'from': accounts[0]})

Transaction sent: 0x54d6708b308d5dc4a06d33380af03c57cd4e76184084bb18ab0a31a653b909b0
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 0
  PuntosFidelizacion.constructor confirmed   Block: 1   Gas used: 1180158 (9.83%)
  PuntosFidelizacion deployed at: 0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87
```

El contrato queda desplegado con un balance de `2*(10**6)` asignados a la dirección `accounts[0]`:

```python
>>> contrato
<PuntosFidelizacion Contract '0x3194cBDC3dbcd3E11a07892e7bA5c3394048Cc87'>

>>> contrato.balanceDePuntos()
2000000000000000000000000

>>> contrato.agregarCliente(accounts[1])
Transaction sent: 0x1572e759ad15309461dcb61e132be6e518fae63c12de1cce453183e628d376f1
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 1
  PuntosFidelizacion.agregarCliente confirmed   Block: 2   Gas used: 24599 (0.20%)

<Transaction '0x1572e759ad15309461dcb61e132be6e518fae63c12de1cce453183e628d376f1'>

>>>>>> contrato.canjearPuntos(150,'id001', {'from':accounts[1]})
Transaction sent: 0x1a7ea9a7ce6df442c175c53dd6176be053cd38da1bc259761d0ae460aa1e2d40
  Gas price: 0.0 gwei   Gas limit: 12000000   Nonce: 0
  PuntosFidelizacion.canjearPuntos confirmed   Block: 3   Gas used: 119842 (1.00%)

<Transaction '0x1a7ea9a7ce6df442c175c53dd6176be053cd38da1bc259761d0ae460aa1e2d40'>
```

## Testing

Para ejecutar los test:

```bash
brownie test
```

Los test que se encuentran actualmente son los que vienen por defecto en la plantilla de brownie y que funcionan con cualquier token ERC20.

## Recursos

Más información sobre Brownie:

* [Brownie mixes](https://github.com/brownie-mix/) template para comenzar proyectos de smart contracts.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) tutorial de Brownie.
* Documentación oficial [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).

