from dataclasses import dataclass
from typing import Optional, Callable

@dataclass
class MultimeterDriver:
    dc_voltage:str
    dc_current:str
    ac_voltage:Optional[str] = None
    ac_current:Optional[str] = None
    ressistance_w2:Optional[str] = None
    ressistance_w4:Optional[str] = None

@dataclass
class PowerSupplyDriver:
    output:str
    dc_voltage:str
    dc_current:str
    internal_multimeter:Optional[str]=None
    on:Optional[str]=None
    off:Optional[str]=None
    ovp:Optional[str]=None
    separator:Optional[str]=None
    power_range:Optional[str] = None
    power_range_low_name:Optional[str] = None
    gestion_sense:Optional[str] = None


@dataclass
class MultiChannelPowerSupply(PowerSupplyDriver):
    channelSelector:Optional[str] = None
    queryChannelContextualise:Callable[[str, str], str] = lambda c, _id: f'{c}?'
    channelContextualise:Callable[[str, str, str], str] = lambda c, v, _id: f'{c} {v}'
    channel_selection:Optional[str] = None

@dataclass
class DynamicLoad:
    output:str
    dc_voltage:str
    dc_current:str
    ressistance:str
    internal_multimeter:MultimeterDriver

STANDART_MULTIMETER_DRIVER = MultimeterDriver (
    dc_voltage="MEASure:VOLTage:DC?",
    ac_voltage="MEASure:VOLTage:AC?",
    dc_current="MEASure:CURRent:DC?",
    ac_current="MEASure:CURRent:AC?",
    ressistance_w2="MEASure:RESistance?",
    ressistance_w4="MEASure:FRESistance?",
)

STANDART_POWER_SUPPLY_DRIVER = PowerSupplyDriver (
   output="OUTPut",
   dc_voltage="VOLTage",
   dc_current="CURRent",
   power_range="VOLT:RANGe",
   on="ON",
   off="OFF",
   internal_multimeter=STANDART_MULTIMETER_DRIVER
)

HP_MAINFRAIM_CHANNEL_POWER_SUPPLY_DRIVER = MultiChannelPowerSupply (
   output="OUTPUT",
   dc_voltage="VOLTage",
   dc_current="CURRent",
   power_range="VOLT:RANGe",
   channelContextualise = lambda c, value, _id: f'{c} {value}, (@{_id})',
   queryChannelContextualise = lambda c, _id: f'{c} (@{_id})',
   internal_multimeter=STANDART_MULTIMETER_DRIVER,
   on="1",
   off="0"
)

HP6060B_DYNAMIC_LOAD_DRIVER = DynamicLoad (
    output=lambda etat:f"OUTPUT{etat}",      # inutile sur cette charge mais c'est pour addapter le fichier procedure pour toutes les charges 
   dc_voltage=lambda value:f"VOLTage {value}",
   dc_current=lambda value:f"CURRent {value}",
   ressistance=lambda value:f"RESistance {value}",
   internal_multimeter=STANDART_MULTIMETER_DRIVER
)

EA_EL_DYNAMIC_LOAD_DRIVER = DynamicLoad (
    output=lambda etat:f"INPut {etat}",
   dc_voltage=lambda value:f"VOLTage {value}",
   dc_current=lambda value:f"CURRent {value}",
   ressistance=lambda value:f"RESistance {value}",
   internal_multimeter=STANDART_MULTIMETER_DRIVER
)




ROHDE_AND_SCHWARZ_STANDART_POWER_SUPPLY_DRIVER = MultiChannelPowerSupply(
    output="OUTPUT",
    dc_voltage="VOLTage",
    dc_current="CURRent",
    power_range="VOLT:RANGe",
    channelSelector="INST:NSEL",
    internal_multimeter=STANDART_MULTIMETER_DRIVER,
    on="1",
    off="0",
    separator= ','

)




ROHDE_AND_SCHWARZ_HMP_MULTICHANNEL_POWER_SUPPLY_DRIVER = MultiChannelPowerSupply(
    output=lambda _id,state:f"OUTPut {state}",
    dc_voltage="VOLTage",
    dc_current="CURRent",
    channelContextualise = lambda unit,_id,value:f"{unit} {value}",
    queryChannelContextualise = lambda unit, _id: f':CHANnel{_id}:MEASure:{unit} ?',
    power_range =  lambda _id, n_range: f'RANGE{_id} {n_range}',  #inutile mais regle de probleme de range dans REGULATION_TENSION
    internal_multimeter= lambda _id,unit:f"MEAS:{unit}?",
    on="1",
    off="0",
    ovp= lambda _id, etat : f"OVP{_id} {etat}",
    channel_selection= lambda _id : f'INST:NSEL {_id} ',
    separator= ',',
    gestion_sense= lambda _id : f'VOLT:SENS EXT'
)



TTI_QL355TP_STANDART_POWER_SUPPLY_DRIVER  = MultiChannelPowerSupply(
    output = lambda _id,state:f"OP{_id} {state}",
    dc_voltage = "V",
    dc_current = "I",
    channelContextualise = lambda unit, _id, value: f'{unit}{_id} {value}',
    queryChannelContextualise = lambda unit, _id: f'{unit}{_id}O?',
    power_range =  lambda _id, n_range: f'RANGE{_id} {n_range}',
    on="1",
    off="0",
    ovp= lambda _id, etat : f"OVP{_id} {etat}",
    separator=";",
    channel_selection= lambda _id : f'{_id}',
    internal_multimeter = lambda _id, unit : f'{unit}{_id}O?',
    gestion_sense= lambda _id :""
    )




KEYSIGHT_8700_STANDART_POWER_SUPPLY_DRIVER  = MultiChannelPowerSupply(
    output = lambda _id,state:f"OUTPut{_id}{state}",
    dc_voltage = "VOLTage",
    dc_current = "CURRent",
    channelContextualise = lambda unit, _id, value: f'{unit}{_id} {value}',
    queryChannelContextualise = lambda unit, _id: f'MEASure:{unit}?{_id}',
    power_range =  lambda _id, n_range: f'VRANGE{_id} {n_range}',
    on="ON",
    off="OFF",
    ovp= lambda _id, etat : f"OVP{_id} {etat}",
    separator=",",
    channel_selection= lambda _id : f'{_id}',
    internal_multimeter = MultimeterDriver(
        dc_voltage = 'V',
        dc_current=  'I'
    )
)


KEYSIGHT_E3632A_STANDART_POWER_SUPPLY_DRIVER  = MultiChannelPowerSupply(
    output = lambda _id,state:f"OUTP {state}",
    dc_voltage = "VOLT",
    dc_current = "CURR",
    channelContextualise = lambda unit, _id, value: f'{unit} {value}',
    queryChannelContextualise = lambda unit, _id: f'MEAS:{unit}?',
    power_range =  lambda _id, n_range: f'VOLT:RANG P{n_range}V',
    on="ON",
    off="OFF",
    ovp= lambda _id, etat : f"OVP{_id} {etat}",
    separator=",",
    channel_selection= lambda _id : f'{_id}',
    gestion_sense= lambda _id : f'VOLT:SENS 1',
    internal_multimeter = MultimeterDriver(
        dc_voltage = 'V',
        dc_current=  'I'
    )
)

KEYSIGHT_E3644A_STANDART_POWER_SUPPLY_DRIVER  = MultiChannelPowerSupply(
    output = lambda _id,state:f"'OUTPut {state}",
    dc_voltage = "VOLT",
    dc_current = "CURR",
    channelContextualise = lambda unit, _id, value: f'{unit} {value}',
    queryChannelContextualise = lambda unit, _id: f'MEAS:{unit}?',
    power_range =  lambda _id, n_range: f'VOLT:RANG P{n_range}V',
    on="1",
    off="0",
    ovp= lambda _id, etat : f"OVP{_id} {etat}",
    separator=",",
    channel_selection= lambda _id : f'{_id}',
    internal_multimeter = MultimeterDriver(
        dc_voltage = 'V',
        dc_current=  'I'
    )
)

TDK_LAMBDA_GENH_STANDART_POWER_SUPPLY_DRIVER  = MultiChannelPowerSupply(
    output = lambda _id,state:f"OUTPut:STATe {state}",
    dc_voltage = "VOLTage",
    dc_current = "CURRent",
    channelContextualise = lambda unit, _id, value: f':{unit} {value}',
    queryChannelContextualise = lambda unit, _id: f'MEASure:{unit}?',
    power_range =  lambda _id, n_range: f'',
    on="1",
    off="0",
    ovp= lambda _id, etat : f"OVP{_id} {etat}",
    separator=",",
    channel_selection= lambda _id : f'{_id}',
    internal_multimeter = MultimeterDriver(
        dc_voltage = 'V',
        dc_current=  'I'
    )
)

AGILENT_N6705A_STANDART_POWER_SUPPLY_DRIVER  = MultiChannelPowerSupply(
    output = lambda _id,state:f'OUTPut {state} , (@{_id})',
    dc_voltage = "VOLTage",
    dc_current = "CURRent",
    channelContextualise = lambda unit, _id, value: f'{unit} {value} , (@{_id})',
    queryChannelContextualise = lambda unit, _id: f'MEASure:{unit}?{_id}',
    power_range =  lambda _id, n_range: f'VOLTage:RANGe {n_range} , (@{_id})',
    on="1",
    off="0",
    ovp= lambda _id, etat : f"OVP{_id} {etat}",
    separator=",",
    channel_selection= lambda _id : '',
    internal_multimeter = MultimeterDriver(
        dc_voltage = 'V',
        dc_current=  'I'
    )
)