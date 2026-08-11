#!/usr/bin/env python3
"""Generate Comparabien wiki concept pages from curated product metadata."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

COUNTRIES = {
    "pe": {
        "code": "PE",
        "name": "Perú",
        "name_local": "Perú",
        "lang": "es",
        "site": "https://comparabien.com.pe",
        "brand": "Comparabien",
    },
    "co": {
        "code": "CO",
        "name": "Colombia",
        "name_local": "Colombia",
        "lang": "es",
        "site": "https://comparabien.com.co",
        "brand": "Comparabien",
    },
    "br": {
        "code": "BR",
        "name": "Brasil",
        "name_local": "Brasil",
        "lang": "pt-BR",
        "site": "https://comparabem.com.br",
        "brand": "Comparabem",
    },
    "mx": {
        "code": "MX",
        "name": "México",
        "name_local": "México",
        "lang": "es",
        "site": "https://comparabien.com.mx",
        "brand": "Comparabien",
    },
    "es": {
        "code": "ES",
        "name": "España",
        "name_local": "España",
        "lang": "es",
        "site": "https://comparabien.es",
        "brand": "Comparabien",
    },
}

# Human labels for common input/output keys (ES default; BR overrides below)
INPUT_LABELS_ES = {
    "balance": ("Saldo o monto", "Cantidad que planeas ahorrar, invertir o depositar."),
    "currency": ("Moneda", "Moneda en la que quieres el producto (local o dólares, según el mercado)."),
    "geo": ("Ubicación / zona", "Ciudad, departamento o región. Puede cambiar precio, disponibilidad o canales."),
    "estado": ("Ubicación / estado", "Entidad federativa o región donde solicitas el producto."),
    "type": ("Tipo de producto", "Variante del producto (por ejemplo libre, vivienda, fondo, plan)."),
    "tipofondo": ("Tipo de fondo", "Perfil del fondo de pensiones (conservador, mixto, etc.)."),
    "metodo": ("Método de cálculo", "Forma de estimar comisiones o rentabilidades en la comparación."),
    "salary": ("Ingreso / sueldo", "Ingreso referencial para filtrar productos que se ajusten a tu perfil."),
    "monto": ("Monto", "Cantidad que quieres financiar, invertir o asegurar."),
    "meses": ("Plazo (meses)", "Cantidad de meses del crédito o del producto."),
    "anos": ("Plazo (años)", "Cantidad de años del crédito o del ahorro programado."),
    "days": ("Plazo (días)", "Duración del depósito o inversión a plazo."),
    "dias": ("Plazo (días)", "Duración del préstamo rápido o microcrédito."),
    "years": ("Horizonte (años)", "Periodo usado para proyectar rentabilidad o cobertura."),
    "minmax": ("Escenario de tasa", "Si prefieres ver el escenario más bajo o más alto de tasa reportada."),
    "brand": ("Marca", "Marca de tarjeta o del vehículo, según el producto."),
    "bonus": ("Beneficio buscado", "Tipo de beneficio que priorizas (millas, cashback, descuentos, etc.)."),
    "model": ("Modelo", "Modelo del vehículo."),
    "variacion": ("Versión", "Versión o variación del vehículo."),
    "year": ("Año del vehículo", "Año de fabricación o modelo del vehículo."),
    "veh_type": ("Tipo de vehículo", "Categoría del vehículo (auto, moto, etc.)."),
    "tipo": ("Tipo / uso", "Clasificación del producto o del uso del vehículo."),
    "uso": ("Uso", "Uso particular o de servicio del vehículo."),
    "uso_moto": ("Uso de moto", "Detalle de uso cuando el vehículo es una moto."),
    "auto": ("Vehículo", "Información del vehículo que quieres financiar."),
    "casa": ("Valor de la vivienda", "Precio o valor de la vivienda relacionada al crédito."),
    "inicial": ("Cuota inicial", "Pago inicial o enganche del financiamiento."),
    "dni": ("Documento de identidad", "Dato opcional para personalizar o validar la comparación."),
    "objetivo_prestamo": ("Objetivo del préstamo", "Para qué necesitas el dinero."),
    "ocupacion": ("Ocupación", "Situación laboral que puede influir en la oferta."),
    "phone": ("Teléfono", "Contacto para seguimiento de la solicitud."),
    "telefono": ("Teléfono", "Contacto para seguimiento de la solicitud."),
    "placa": ("Placa", "Placa del vehículo cuando la cotización lo requiere."),
    "price": ("Valor asegurado", "Valor referencial del vehículo o bien a asegurar."),
    "vehiculo": ("Vehículo", "Datos del vehículo a asegurar."),
    "combustible": ("Combustible", "Tipo de combustible del vehículo."),
    "news": ("Vehículo nuevo o usado", "Si el auto es 0 km o de segunda mano."),
    "cover": ("Cobertura", "Nivel o tipo de cobertura que buscas."),
    "cot": ("Cotización", "Identificador de cotización previa, si aplica."),
    "partner": ("Canal / aliado", "Canal comercial desde el que llegas a la comparación."),
    "user_company_insurance": ("Aseguradora actual", "Compañía con la que tienes seguro hoy, si aplica."),
    "edad": ("Edad", "Edad del asegurado o titular."),
    "edades": ("Edades del grupo", "Edades de las personas a incluir en el plan."),
    "sexos": ("Sexo / género", "Dato demográfico usado en tarifas de salud."),
    "cantidad": ("Cantidad de personas", "Número de asegurados o beneficiarios."),
    "fumador": ("Fumador", "Si la persona fuma; puede cambiar el precio."),
    "clinicas": ("Clínicas preferidas", "Red de clínicas o hospitales que te interesan."),
    "id_clinicas": ("Clínicas seleccionadas", "Lista concreta de clínicas elegidas en el filtro."),
    "nivel": ("Nivel de plan", "Categoría del plan de salud."),
    "cuota_maxima": ("Cuota máxima", "Tope mensual que estás dispuesto a pagar."),
    "capital": ("Capital / suma", "Monto de cobertura o capital asegurado buscado."),
    "tamano_terreno": ("Tamaño del terreno", "Dimensión del inmueble o terreno."),
    "tipo_cobertura": ("Tipo de cobertura", "Alcance del seguro de hogar."),
    "tipo_inmueble": ("Tipo de inmueble", "Casa, departamento u otra categoría."),
    "tipo_plan": ("Tipo de plan", "Variante del plan de seguro."),
    "valor_contenido": ("Valor del contenido", "Valor estimado de bienes dentro del hogar."),
    "valor_inmueble": ("Valor del inmueble", "Valor estimado de la vivienda."),
    "pension": ("Aporte / pensión", "Monto relacionado a aportes o proyección pensionaria."),
    "monto1": ("Monto del certificado", "Valor del bien o certificado del fondo colectivo."),
    "credit": ("Límite de crédito", "Límite o uso de crédito que te interesa en la tarjeta."),
    "cep": ("CEP / código postal", "Ubicación para filtrar ofertas locales."),
    "celular": ("Celular", "Número de contacto para la solicitud."),
    "bcb": ("Referencia regulatoria", "Indicador usado para contextualizar tasas del mercado."),
    "modal": ("Modalidad", "Formato de la oferta o flujo de solicitud."),
    "acomoda": ("Acomodación", "Tipo de habitación o acomodación del plan de salud."),
    "aseg": ("Asegurados", "Perfil de quienes serán cubiertos."),
    "assist": ("Asistencia", "Si buscas asistencia adicional en el plan."),
    "choice": ("Preferencia de red", "Cómo priorizas hospitales o cobertura geográfica."),
    "copart": ("Copago", "Si aceptas o prefieres planes con copago."),
    "geotip": ("Alcance geográfico", "Municipal, estadual o nacional."),
    "municipio": ("Municipio", "Ciudad/municipio para la red de atención."),
}

INPUT_LABELS_PT = {
    **INPUT_LABELS_ES,
    "balance": ("Saldo ou valor", "Quanto você pretende poupar, investir ou depositar."),
    "currency": ("Moeda", "Moeda do produto."),
    "geo": ("Localização", "Cidade ou região. Pode mudar preço e disponibilidade."),
    "estado": ("Estado", "Unidade federativa onde você solicita o produto."),
    "type": ("Tipo de produto", "Variante do produto."),
    "salary": ("Renda", "Renda de referência para filtrar ofertas."),
    "monto": ("Valor", "Quanto você quer financiar, investir ou assegurar."),
    "meses": ("Prazo (meses)", "Quantidade de meses do crédito ou produto."),
    "anos": ("Prazo (anos)", "Quantidade de anos do financiamento."),
    "days": ("Prazo (dias)", "Duração do CDB ou aplicação."),
    "minmax": ("Cenário de taxa", "Cenário mais baixo ou mais alto da taxa."),
    "brand": ("Bandeira / marca", "Bandeira do cartão ou marca do veículo."),
    "bonus": ("Benefício desejado", "Tipo de benefício que você prioriza."),
    "auto": ("Veículo", "Dados do veículo a financiar."),
    "casa": ("Valor do imóvel", "Preço do imóvel relacionado ao financiamento."),
    "inicial": ("Entrada", "Valor de entrada do financiamento."),
    "cep": ("CEP", "Localização para filtrar ofertas."),
    "celular": ("Celular", "Contato para a solicitação."),
    "cover": ("Cobertura", "Nível de cobertura desejado."),
    "cantidad": ("Quantidade de pessoas", "Número de beneficiários."),
    "clinicas": ("Hospitais preferidos", "Rede hospitalar de interesse."),
    "acomoda": ("Acomodação", "Tipo de quarto do plano."),
    "copart": ("Coparticipação", "Se você aceita planos com coparticipação."),
    "geotip": ("Abrangência", "Municipal, estadual ou nacional."),
    "municipio": ("Município", "Cidade para a rede de atendimento."),
    "choice": ("Preferência de rede", "Como priorizar hospitais ou cobertura."),
}

OUTPUT_LABELS_ES = {
    "COMPANY_NAME": ("Entidad / compañía", "Banco, financiera o aseguradora que ofrece el producto."),
    "PRODUCT_NAME": ("Nombre del producto", "Nombre comercial de la oferta."),
    "UPDATE_DT": ("Fecha de actualización", "Cuándo se actualizó la información mostrada."),
    "TEA": ("TEA / tasa efectiva", "Tasa efectiva anual referencial del producto."),
    "TEA_MAX": ("TEA máxima", "Tope alto de la tasa efectiva anual reportada."),
    "TEA_MIN": ("TEA mínima", "Tope bajo de la tasa efectiva anual reportada."),
    "TEA_MN": ("TEA en moneda local", "Tasa efectiva en moneda nacional."),
    "TEA_MN_MAX": ("TEA máx. moneda local", "Tasa alta en moneda nacional (compras)."),
    "TEA_MN_MIN": ("TEA mín. moneda local", "Tasa baja en moneda nacional (compras)."),
    "TEA_ME_MAX": ("TEA máx. moneda extranjera", "Tasa alta en moneda extranjera."),
    "TEA_ME_MIN": ("TEA mín. moneda extranjera", "Tasa baja en moneda extranjera."),
    "TCEA": ("TCEA", "Costo efectivo total anual, incluye más cargos además de la tasa."),
    "TIN": ("TIN", "Tipo de interés nominal."),
    "TAE": ("TAE", "Tasa anual equivalente."),
    "TEM": ("TEM", "Tasa efectiva mensual referencial."),
    "TEM_MAX": ("TEM máxima", "Tasa mensual alta del escenario."),
    "TEM_MIN": ("TEM mínima", "Tasa mensual baja del escenario."),
    "TN_MAX": ("TIN máxima", "Tipo de interés nominal alto."),
    "TN_MIN": ("TIN mínima", "Tipo de interés nominal bajo."),
    "CUOTA": ("Cuota", "Pago periódico estimado."),
    "CUOTA_MENSUAL": ("Cuota mensual", "Pago mensual estimado."),
    "PAGO": ("Pago total", "Monto a devolver o pagar en el escenario simulado."),
    "PAGO_TOT": ("Pago total", "Costo total estimado del crédito."),
    "PAGO_TOTAL": ("Pago total", "Costo total estimado del crédito."),
    "PAGO_MENSUAL": ("Pago mensual", "Aporte o cuota mensual del producto."),
    "MAIL_COST": ("Costo de envío / mantención", "Cargo adicional periódico asociado al producto."),
    "MAIN_COST": ("Costo de mantenimiento", "Comisión o costo de mantener la cuenta/producto."),
    "INITIAL_COST": ("Costo inicial", "Cargo de apertura o inicio."),
    "INI_COST": ("Costes iniciales", "Gastos de constitución o apertura."),
    "COMISION": ("Comisión", "Cargo porcentual o fijo de la operación."),
    "INS_COST": ("Seguro / costo de seguro", "Componente de seguro asociado al crédito."),
    "INS_AUTO": ("Seguro vehicular", "Seguro del vehículo ligado al financiamiento."),
    "INS_HOUSE": ("Seguro de inmueble", "Seguro de la vivienda ligado a la hipoteca."),
    "MINIMO_AP": ("Monto mínimo", "Mínimo para abrir o contratar."),
    "OPEN_MIN": ("Monto mínimo de apertura", "Inversión mínima para entrar al fondo."),
    "PLAZO": ("Plazo", "Duración del producto."),
    "PLAZO_MAX": ("Plazo máximo", "Duración máxima disponible."),
    "PLAZO_MIN": ("Plazo mínimo", "Duración mínima disponible."),
    "GANANCIA": ("Ganancia estimada", "Resultado estimado según el escenario."),
    "GANANCIA_TOTAL": ("Ganancia total", "Rendimiento estimado al final del plazo."),
    "GANANCIA_MENSUAL": ("Ganancia mensual", "Rendimiento mensual estimado."),
    "FSD": ("Fondo de seguro de depósitos", "Si el producto está cubierto por el fondo de garantía."),
    "ONLINE": ("Apertura online", "Si puedes abrir o solicitar el producto por internet."),
    "OP_ATM": ("Operaciones en cajero", "Disponibilidad de operaciones en ATM."),
    "OP_VENTANILLA": ("Operaciones en ventanilla", "Disponibilidad de operaciones en agencia."),
    "PROMO": ("Promoción", "Beneficio temporal o campaña vigente."),
    "BENEFITS": ("Beneficios", "Ventajas o extras de la oferta."),
    "BENEFICIOS": ("Beneficios", "Ventajas o extras de la oferta."),
    "BENEFITS2": ("Beneficios adicionales", "Capa extra de coberturas o ventajas."),
    "BONUS": ("Beneficios de la tarjeta", "Programa de beneficios asociado."),
    "BRAND": ("Marca / franquicia", "Visa, Mastercard u otra marca."),
    "ANNUAL_COST": ("Costo anual / membresía", "Costo anual de la tarjeta o membresía."),
    "MONTH_COST": ("Costo mensual", "Cargos mensuales asociados."),
    "SALARIO_MIN": ("Ingreso mínimo", "Ingreso mínimo sugerido para la tarjeta."),
    "DEUDA_MN_MAX": ("Tasa traslado de deuda (máx.)", "TEA alta para consolidar o trasladar deuda."),
    "DEUDA_MN_MIN": ("Tasa traslado de deuda (mín.)", "TEA baja para consolidar o trasladar deuda."),
    "DEUDA_TEA_MAX": ("Tasa traslado de deuda (máx.)", "TEA alta para traslado de deuda."),
    "DEUDA_TEA_MIN": ("Tasa traslado de deuda (mín.)", "TEA baja para traslado de deuda."),
    "EFECT_MN_MAX": ("Tasa de avance/efectivo (máx.)", "TEA alta para disposición de efectivo."),
    "EFECT_MN_MIN": ("Tasa de avance/efectivo (mín.)", "TEA baja para disposición de efectivo."),
    "EFECTIVO_TEA_MAX": ("Tasa de avance/efectivo (máx.)", "TEA alta para disposición de efectivo."),
    "EFECTIVO_TEA_MIN": ("Tasa de avance/efectivo (mín.)", "TEA baja para disposición de efectivo."),
    "PRICE": ("Precio", "Precio o prima del seguro."),
    "PRIMA": ("Prima", "Costo del seguro o plan."),
    "PRIME": ("Prima", "Costo del seguro."),
    "PRIMA_ORIGINAL": ("Prima original", "Prima antes de descuentos."),
    "MONTHLY_PRICE": ("Precio mensual", "Cuota mensual del seguro o plan."),
    "ANNUAL_PRICE": ("Precio anual", "Costo anual del seguro o plan."),
    "ANUAL": ("Pago anual", "Opción o monto de pago anual."),
    "MONTH": ("Pago mensual", "Opción o monto de pago mensual."),
    "MENSUAL": ("Prima mensual", "Costo mensual del seguro de vida."),
    "PRIM_MENS": ("Prima mensual", "Prima mensual referencial."),
    "DESCR": ("Descripción", "Resumen de la oferta."),
    "COMMENT": ("Comentarios", "Notas importantes sobre la oferta."),
    "EXCLUSIVE": ("Oferta exclusiva", "Si la oferta es especial por canal o zona."),
    "COBERTURA": ("Cobertura", "Alcance de la protección."),
    "COVER": ("Cobertura", "Qué protege el plan."),
    "COVERS": ("Coberturas", "Lista de coberturas incluidas."),
    "COVERAGES": ("Coberturas", "Detalle de coberturas del plan."),
    "COVERAGE": ("Cobertura", "Alcance del seguro de hogar."),
    "SUM_INSURED": ("Suma asegurada", "Monto máximo de cobertura."),
    "SUMA_ASEGURADA": ("Suma asegurada", "Monto máximo de cobertura."),
    "GEO_COVERAGE": ("Cobertura geográfica", "Dónde aplica la red o el seguro."),
    "CLINICS": ("Clínicas / red", "Red de atención incluida."),
    "TOTAL_CLINICS": ("Cantidad de clínicas", "Tamaño de la red."),
    "HOSPITAIS": ("Hospitais", "Rede hospitalar do plano."),
    "CANT_HOSPITAIS": ("Qtde. de hospitais", "Tamanho da rede hospitalar."),
    "MUNICIPIOS": ("Municípios", "Cidades cobertas."),
    "CANT_MUNICIPIOS": ("Qtde. de municípios", "Abrangência municipal."),
    "ESTADOS": ("Estados", "Estados cobertos pelo plano."),
    "ROOM_TYPE": ("Tipo de acomodação", "Apartamento, enfermaria, etc."),
    "COPART": ("Coparticipação", "Se o plano tem coparticipação."),
    "TIPO_PLAN": ("Tipo de plano", "Categoria do plano de saúde."),
    "OBSTETRICIA": ("Obstetrícia", "Se inclui cobertura obstétrica."),
    "RESTRICTION": ("Restricciones", "Limitaciones o exclusiones relevantes."),
    "AGE_MIN": ("Edad mínima", "Edad mínima de ingreso."),
    "AGE_MAX": ("Edad máxima", "Edad máxima de ingreso."),
    "SMOKER": ("Condición de fumador", "Si el plan diferencia tarifas por hábito de fumar."),
    "DISCOUNT": ("Descuento", "Descuento aplicado a la prima."),
    "SURVIVAL": ("Sobrevida / continuidad", "Condiciones de continuidad de cobertura."),
    "AMB": ("Ambulatorio", "Cobertura ambulatoria."),
    "HOS": ("Hospitalario", "Cobertura hospitalaria."),
    "TYPE": ("Tipo", "Clasificación del producto o plan."),
    "TIPO": ("Tipo", "Clasificación del producto."),
    "FINANCE": ("Monto a financiar", "Parte del valor que realmente se financia."),
    "FINANC": ("Monto a financiar", "Parte del valor que realmente se financia."),
    "LOCATION": ("Disponibilidad geográfica", "Dónde aplica o se comercializa la oferta."),
    "TIEMPO_APROBACION": ("Tiempo de aprobación", "Rapidez estimada de respuesta."),
    "INT_DIARIO": ("Interés diario", "Costo diario referencial del préstamo rápido."),
    "INT_COM": ("Interés / comisión", "Componente de interés o comisión del microcrédito."),
    "CAT": ("CAT", "Costo Anual Total (México/España según mercado)."),
    "ADM": ("Administración", "Cargo administrativo."),
    "INS": ("Seguro", "Seguro asociado al préstamo rápido."),
    "PLT": ("Plataforma / canal", "Canal de originación."),
    "TRN": ("Transferencia / desembolso", "Condición de desembolso."),
    "RENT_1": ("Rentabilidad 1 año", "Rendimiento referencial a 1 año."),
    "RENT_2": ("Rentabilidad 2 años", "Rendimiento referencial a 2 años."),
    "RENT_3": ("Rentabilidad 3 años", "Rendimiento referencial a 3 años."),
    "RENT_5": ("Rentabilidad 5 años", "Rendimiento referencial a 5 años."),
    "RENT_10": ("Rentabilidad 10 años", "Rendimiento referencial a 10 años."),
    "RENT_M": ("Rentabilidad del mes", "Rendimiento reciente del periodo corto."),
    "R1": ("Rentabilidad 1 año", "Rendimiento referencial a 1 año."),
    "R2": ("Rentabilidad 2 años", "Rendimiento referencial a 2 años."),
    "R3": ("Rentabilidad 3 años", "Rendimiento referencial a 3 años."),
    "R5": ("Rentabilidad 5 años", "Rendimiento referencial a 5 años."),
    "R10": ("Rentabilidad 10 años", "Rendimiento referencial a 10 años."),
    "APORTE": ("Aporte", "Aporte o comisión relacionada a la AFP."),
    "COM_REM": ("Comisión sobre remuneración", "Comisión por flujo de aportes."),
    "COM_REM_MIX": ("Comisión mixta (remuneración)", "Componente mixto sobre remuneración."),
    "COM_SA_MIX": ("Comisión mixta (saldo)", "Componente mixto sobre saldo."),
    "INS_COST_REM": ("Prima de seguro", "Componente de seguro previsional."),
    "CTS_SUELDO": ("Relación con sueldo", "Condiciones vinculadas a cuenta sueldo."),
    "CTS_SIN_DEP": ("Sin depósito mínimo", "Si permite operar sin depósito mínimo."),
    "TRAS_PRE": ("Traslado desde otra entidad", "Condiciones para traer tu CTS."),
    "TRAS_SUE": ("Traslado con sueldo", "Condiciones ligadas a planilla/sueldo."),
    "COSTO_TOTAL": ("Costo total", "Costo total del fondo colectivo o consorcio."),
    "VALOR_CERTIFICADO": ("Valor del certificado", "Monto del bien o crédito del consorcio."),
    "PORC_INSCRIPCION": ("% de inscripción", "Porcentaje de inscripción al fondo colectivo."),
    "TASA_ADMIN": ("Tasa de administración", "Costo de administrar el consorcio."),
    "FIRST_MONTH": ("Primera cuota", "Pago del primer mes."),
    "SUB_PRODUCT": ("Subproducto", "Variante dentro del consorcio."),
    "COB": ("Coberturas", "Qué cubre el seguro de vida."),
    "DEVOLUCION": ("Devolución", "Si el producto contempla devolución de prima."),
    "DEV_FINAL": ("Devolución final", "Monto o condición de devolución al final."),
    "MONT_MIN_AP": ("Aporte mínimo", "Mínimo para contratar."),
    "TASA": ("Tasa", "Tasa o costo referencial del seguro."),
    "PLAN": ("Plan", "Nombre del plan de seguro vehicular."),
    "SHARE": ("Deducible", "Participación del asegurado en el siniestro."),
    "SHARE_MIN": ("Deducible mínimo", "Piso del deducible."),
    "NUM_SHARE": ("Cuotas de prima", "En cuántas cuotas puedes pagar la prima."),
    "DESCUENTO": ("Descuento", "Descuento sobre la prima."),
    "TOTAL_THEFT": ("Pérdida total por robo", "Cobertura ante robo total."),
    "NATURE": ("Daños por naturaleza", "Cobertura ante eventos de la naturaleza."),
    "MEDICAL": ("Gastos médicos", "Cobertura médica del seguro auto."),
    "DEATH": ("Muerte accidental", "Cobertura por fallecimiento en accidente."),
    "REPLACE_AUTO": ("Reposición del vehículo", "Condiciones de reemplazo del auto."),
    "REPLACE_DRIVER": ("Conductor de reemplazo", "Asistencia de conductor sustituto."),
    "FULL": ("Cobertura amplia", "Si el plan es de cobertura amplia."),
    "CURRENCY": ("Moneda de la prima", "Moneda en la que se cotiza."),
    "CURR_EXCHANGE": ("Tipo de cambio", "Referencia cambiaria usada en la cotización."),
    "RUNT": ("RUNT / registro", "Información vinculada al registro vehicular."),
    "NUM_BENEFITS": ("Cantidad de beneficios", "Número de beneficios destacados."),
    "CONT": ("Contenido / detalle", "Detalle adicional de la oferta SOAT."),
    "CET": ("CET", "Custo Efetivo Total do crédito."),
    "BCB": ("Referência de mercado", "Indicador de contexto de taxas."),
    "TASA_MORATORIA": ("Taxa de mora", "Custo em caso de atraso."),
    "SALARY_PC": ("% da renda", "Comprometimento estimado da renda."),
    "PROD_TYPE": ("Tipo de empréstimo", "Categoria do crédito."),
    "ADM_COST": ("Taxa de administração", "Custo administrativo do consórcio."),
    "COSTO_TOT": ("Custo total", "Custo total estimado."),
    "RESERV_COST": ("Fundo de reserva", "Componente de reserva do consórcio."),
    "MES_TOT": ("Prazo total (meses)", "Duração total do consórcio."),
    "MONTO": ("Valor", "Valor do crédito ou bem."),
    "IRN": ("IRN", "Indicador de rendimiento neto de la Afore."),
    "REND_12": ("Rendimiento 12 meses", "Rendimiento a 12 meses."),
    "REND_24": ("Rendimiento 24 meses", "Rendimiento a 24 meses."),
    "REND_36": ("Rendimiento 36 meses", "Rendimiento a 36 meses."),
    "REND_5A": ("Rendimiento 5 años", "Rendimiento a 5 años."),
    "INCREASE": ("Incremento / ajuste", "Cómo puede variar la cuota en el tiempo."),
    "PAY_MIL": ("Pago por mil", "Referencia de pago por cada mil de crédito."),
    "EURIBOR": ("Euríbor", "Índice de referencia de hipotecas variables."),
    "MON_MAX": ("Monto máximo", "Tope que puedes solicitar."),
    "SERVICES": ("Serviços da conta", "Serviços inclusos na conta corrente."),
    "AI_DED_RCE_ORIG": ("Deducible RCE", "Deducible de responsabilidad civil."),
    "AI_DED_TOTAL_LOSS_ORIG": ("Deducible pérdida total", "Deducible ante pérdida total."),
    "AI_DED_TOTAL_THEFT_ORIG": ("Deducible robo total", "Deducible ante robo total."),
    "AI_DED_PARTIAL_LOSS_ORIG": ("Deducible pérdida parcial", "Deducible ante daño parcial."),
    "AI_DED_PARTIAL_THEFT_ORIG": ("Deducible robo parcial", "Deducible ante robo parcial."),
    "AI_DED_NATURE_ORIG": ("Deducible eventos naturales", "Deducible ante fenómenos naturales."),
}

OUTPUT_LABELS_PT = {
    **OUTPUT_LABELS_ES,
    "COMPANY_NAME": ("Instituição", "Banco, financeira ou seguradora."),
    "PRODUCT_NAME": ("Nome do produto", "Nome comercial da oferta."),
    "UPDATE_DT": ("Data de atualização", "Quando a informação foi atualizada."),
    "TEA": ("Taxa efetiva", "Taxa efetiva anual de referência."),
    "TEA_MAX": ("Taxa máxima", "Teto alto da taxa."),
    "TEA_MIN": ("Taxa mínima", "Teto baixo da taxa."),
    "CUOTA": ("Parcela", "Valor estimado da parcela."),
    "PAGO_TOT": ("Pagamento total", "Custo total estimado."),
    "PAGO_TOTAL": ("Pagamento total", "Custo total estimado."),
    "MINIMO_AP": ("Valor mínimo", "Mínimo para contratar."),
    "GANANCIA_TOTAL": ("Rendimento total", "Ganho estimado ao fim do prazo."),
    "BENEFITS": ("Benefícios", "Vantagens da oferta."),
    "ANNUAL_COST": ("Anuidade", "Custo anual do cartão."),
    "SALARIO_MIN": ("Renda mínima", "Renda mínima sugerida."),
    "PRIMA": ("Prêmio / mensalidade", "Custo do plano ou seguro."),
}

# Skip noisy/internal-ish inputs
SKIP_INPUTS = {
    "iSortCol_0",
    "iSortingCols",
    "sSortDir_0",
    "partners",
    "partners_cuota",
    "partners_id_oferta",
    "partners_monto",
    "partners_plazo",
    "partners_tasa",
    "partners_url",
    "modal",
    "cot",
    "partner",
    "user_company_insurance",
    "phone",
    "telefono",
    "celular",
    "dni",
    "id_clinicas",
    "sexos",
    "bcb",
}

# Prefer a curated subset of outputs when too many
PREFERRED_OUTPUTS = [
    "COMPANY_NAME",
    "PRODUCT_NAME",
    "PRICE",
    "PRIMA",
    "PRIME",
    "MONTHLY_PRICE",
    "ANNUAL_PRICE",
    "CUOTA",
    "CUOTA_MENSUAL",
    "TEA",
    "TEA_MIN",
    "TEA_MAX",
    "TCEA",
    "TIN",
    "TAE",
    "TEM",
    "CAT",
    "CET",
    "PAGO",
    "PAGO_TOT",
    "PAGO_TOTAL",
    "GANANCIA_TOTAL",
    "GANANCIA",
    "MINIMO_AP",
    "OPEN_MIN",
    "ANNUAL_COST",
    "MONTH_COST",
    "SALARIO_MIN",
    "BONUS",
    "BENEFITS",
    "BENEFICIOS",
    "COVER",
    "COVERAGE",
    "COBERTURA",
    "SUM_INSURED",
    "SUMA_ASEGURADA",
    "PLAZO",
    "PLAZO_MIN",
    "PLAZO_MAX",
    "TIEMPO_APROBACION",
    "FINANCE",
    "INS_COST",
    "INS_AUTO",
    "INS_HOUSE",
    "MAIN_COST",
    "FSD",
    "RENT_1",
    "RENT_3",
    "RENT_5",
    "IRN",
    "REND_12",
    "EURIBOR",
    "HOSPITAIS",
    "GEO_COVERAGE",
    "UPDATE_DT",
]


def labels_for(lang: str):
    if lang.startswith("pt"):
        return INPUT_LABELS_PT, OUTPUT_LABELS_PT
    return INPUT_LABELS_ES, OUTPUT_LABELS_ES


def pick_outputs(outputs: list[str]) -> list[str]:
    preferred = [o for o in PREFERRED_OUTPUTS if o in outputs]
    extras = [o for o in outputs if o not in preferred]
    # keep preferred + a few extras for richness, capped
    merged = preferred + extras
    # always try to keep company/product/update if present
    return merged[:12]


PRODUCTS = [
    # PE
    {"country": "pe", "slug": "soat", "file": "soat.html", "title": "SOAT", "category": "Seguros", "path": "/soat", "blurb": "Seguro Obligatorio de Accidentes de Tránsito: precio por zona, uso del vehículo y beneficios.", "summary": "El SOAT cubre lesiones a personas en un accidente de tránsito. Comparabien te muestra variables que cambian el precio y la cobertura.", "inputs": ["tipo", "veh_type", "uso", "brand", "model", "variacion", "year", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PRICE", "DESCR", "BENEFITS", "COMMENT", "EXCLUSIVE", "UPDATE_DT"], "tips": ["Define primero el uso y la zona: suelen mover más el precio.", "Si dos precios están cerca, revisa beneficios y comentarios.", "Solicita desde Comparabien para ir directo a la opción elegida."]},
    {"country": "pe", "slug": "tarjetas-credito", "file": "tarjetas-credito.html", "title": "Tarjetas de crédito", "category": "Tarjetas", "path": "/tarjetas-de-credito", "blurb": "Membresía, tasas, ingreso mínimo y beneficios de tarjetas.", "summary": "Una tarjeta de crédito combina costo de membresía, tasas de interés y beneficios. Comparabien ordena opciones según tu ingreso y la marca que prefieres.", "inputs": ["salary", "brand", "bonus", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "BRAND", "ANNUAL_COST", "MONTH_COST", "SALARIO_MIN", "TEA_MN_MIN", "TEA_MN_MAX", "BONUS", "UPDATE_DT"], "tips": ["Prioriza el beneficio que realmente usarás (no todos los bonus sirven igual).", "Compara membresía + tasa, no solo una de las dos.", "Revisa tasas de compras, efectivo y traslado de deuda por separado."]},
    {"country": "pe", "slug": "prestamos-personales", "file": "prestamos-personales.html", "title": "Préstamos personales", "category": "Préstamos", "path": "/prestamos-personales", "blurb": "Monto, plazo, TEA y cuota de préstamos personales.", "summary": "Un préstamo personal te da liquidez a cambio de una cuota. Comparabien estima cuotas y tasas según monto, plazo e ingreso.", "inputs": ["monto", "meses", "salary", "currency", "type", "geo", "objetivo_prestamo", "ocupacion", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "TCEA", "INS_COST", "PAGO_TOT", "UPDATE_DT"], "tips": ["Fija primero monto y plazo; luego compara cuota y TCEA.", "Un TEA bajo no siempre es la mejor opción si hay seguros o cargos altos.", "Revisa si el producto exige perfil o zona específica."]},
    {"country": "pe", "slug": "prestamos-rapidos", "file": "prestamos-rapidos.html", "title": "Préstamos rápidos", "category": "Préstamos", "path": "/prestamos-rapidos", "blurb": "Microcréditos de corto plazo: interés, comisión y tiempo de aprobación.", "summary": "Los préstamos rápidos priorizan velocidad de desembolso. Comparabien muestra costo y tiempo de aprobación para montos y plazos cortos.", "inputs": ["monto", "dias", "currency", "type", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PAGO", "INT_DIARIO", "COMISION", "TCEA", "TIEMPO_APROBACION", "UPDATE_DT"], "tips": ["Úsalos solo para necesidades de muy corto plazo.", "Compara el pago total, no solo el interés diario.", "El tiempo de aprobación importa, pero no más que el costo."]},
    {"country": "pe", "slug": "creditos-hipotecarios", "file": "creditos-hipotecarios.html", "title": "Créditos hipotecarios", "category": "Préstamos", "path": "/creditos-hipotecarios", "blurb": "Cuota, TEA, seguros y financiamiento de vivienda.", "summary": "Un crédito hipotecario financia tu vivienda a largo plazo. Comparabien estima cuota, tasas y costos asociados según monto, plazo e ingreso.", "inputs": ["monto", "anos", "salary", "currency", "type", "casa", "geo", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "TCEA", "FINANCE", "INS_HOUSE", "INS_COST", "UPDATE_DT"], "tips": ["Mira la cuota mensual y también seguros ligados a la hipoteca.", "El porcentaje financiado puede diferir del valor total de la casa.", "Compara TCEA para ver el costo más completo."]},
    {"country": "pe", "slug": "creditos-vehiculares", "file": "creditos-vehiculares.html", "title": "Créditos vehiculares", "category": "Préstamos", "path": "/creditos-vehiculares", "blurb": "Financiamiento de autos: cuota, TEA y seguros.", "summary": "El crédito vehicular financia la compra de un auto. Comparabien estima cuotas y costos según monto, plazo y perfil.", "inputs": ["monto", "meses", "salary", "currency", "auto", "geo", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "TCEA", "INS_AUTO", "PAGO_TOT", "UPDATE_DT"], "tips": ["Incluye el seguro del auto en tu comparación de costo total.", "Plazos más largos bajan la cuota pero suben el interés pagado.", "Confirma si tu zona o perfil limita algunas ofertas."]},
    {"country": "pe", "slug": "seguros-vehiculares", "file": "seguros-vehiculares.html", "title": "Seguros vehiculares", "category": "Seguros", "path": "/seguros-vehiculares", "blurb": "Prima, coberturas, deducibles y beneficios del seguro de auto.", "summary": "El seguro vehicular protege tu auto ante daños, robo y responsabilidad. Comparabien cotiza planes según vehículo, zona y cobertura.", "inputs": ["brand", "model", "variacion", "year", "price", "geo", "cover", "combustible", "news", "placa", "vehiculo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PLAN", "PRIMA_ORIGINAL", "DESCUENTO", "SHARE", "BENEFITS", "TOTAL_THEFT", "NATURE", "UPDATE_DT"], "tips": ["No compares solo prima: revisa deducible y coberturas clave.", "Robo total, daños por naturaleza y asistencia suelen marcar la diferencia.", "Ten a mano marca, modelo, año y valor del vehículo."]},
    {"country": "pe", "slug": "seguros-salud", "file": "seguros-salud.html", "title": "Seguros de salud", "category": "Seguros", "path": "/seguros-de-salud", "blurb": "Planes de salud por precio, red de clínicas y coberturas.", "summary": "Un seguro de salud combina precio, red de clínicas y alcance de cobertura. Comparabien filtra planes según edades, zona y preferencias de atención.", "inputs": ["cantidad", "edades", "geo", "clinicas", "cover", "nivel", "cuota_maxima"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "MONTHLY_PRICE", "ANUAL", "CLINICS", "COVERS", "GEO_COVERAGE", "SUM_INSURED", "RESTRICTION", "UPDATE_DT"], "tips": ["Primero elige la red de clínicas que te importa.", "Compara precio mensual y restricciones de edad o preexistencias.", "Una cuota baja puede limitar hospitales o coberturas."]},
    {"country": "pe", "slug": "seguros-oncologicos", "file": "seguros-oncologicos.html", "title": "Seguros oncológicos", "category": "Seguros", "path": "/seguros-oncologicos", "blurb": "Cobertura oncológica: prima, suma asegurada y restricciones.", "summary": "Los seguros oncológicos se enfocan en cobertura ante cáncer. Comparabien muestra prima, suma asegurada y condiciones según edad y perfil.", "inputs": ["edad", "cantidad", "fumador", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "MONTHLY_PRICE", "ANNUAL_PRICE", "SUM_INSURED", "AGE_MIN", "AGE_MAX", "RESTRICTION", "SMOKER", "UPDATE_DT"], "tips": ["Revisa suma asegurada y restricciones antes que el precio solo.", "Edad y hábito de fumar pueden cambiar la prima.", "Lee bien límites de edad de ingreso."]},
    {"country": "pe", "slug": "seguros-vida", "file": "seguros-vida.html", "title": "Seguros de vida", "category": "Seguros", "path": "/seguros-de-vida", "blurb": "Prima, suma asegurada y beneficios del seguro de vida.", "summary": "El seguro de vida protege a tus beneficiarios ante fallecimiento u otros eventos según el plan. Comparabien contrasta prima y suma asegurada.", "inputs": ["capital", "years", "tipo", "currency", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "SUMA_ASEGURADA", "PRIM_MENS", "ANUAL", "COB", "BENEFICIOS", "DEVOLUCION", "UPDATE_DT"], "tips": ["Define primero la suma asegurada que necesitas proteger.", "Compara prima mensual vs. anual y si hay devolución.", "Revisa qué coberturas extras incluye cada plan."]},
    {"country": "pe", "slug": "seguros-hogar", "file": "seguros-hogar.html", "title": "Seguros de hogar", "category": "Seguros", "path": "/seguros-hogar", "blurb": "Protección de vivienda y contenido: prima y coberturas.", "summary": "El seguro de hogar protege inmueble y/o contenido. Comparabien estima cuotas según tipo de inmueble, valores y cobertura.", "inputs": ["tipo_inmueble", "tipo_cobertura", "tipo_plan", "valor_inmueble", "valor_contenido", "tamano_terreno", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PRIME", "CUOTA_MENSUAL", "COVERAGE", "BENEFITS", "NUM_SHARE", "UPDATE_DT"], "tips": ["Separa valor de inmueble y de contenido al comparar.", "Revisa qué eventos cubre el plan (robo, incendio, etc.).", "La forma de pago en cuotas también cambia el costo percibido."]},
    {"country": "pe", "slug": "depositos-plazo", "file": "depositos-plazo.html", "title": "Depósitos a plazo", "category": "Ahorros", "path": "/depositos-a-plazo", "blurb": "TEA, plazo y ganancia estimada de depósitos a plazo.", "summary": "Un depósito a plazo fija tu dinero por un tiempo a cambio de una tasa. Comparabien estima ganancia según monto y días.", "inputs": ["balance", "days", "currency", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "GANANCIA_TOTAL", "GANANCIA_MENSUAL", "MINIMO_AP", "PLAZO_MIN", "PLAZO_MAX", "FSD", "UPDATE_DT"], "tips": ["Compara TEA y ganancia total para tu plazo exacto.", "Verifica monto mínimo y si hay cobertura del fondo de depósitos.", "Plazos más largos no siempre son automáticamente mejores."]},
    {"country": "pe", "slug": "depositos-pension", "file": "depositos-pension.html", "title": "Depósitos para pensión", "category": "Ahorros", "path": "/depositos-para-pension", "blurb": "Ahorro programado para pensión: TEA, plazos y aportes.", "summary": "Los depósitos para pensión ayudan a construir un ahorro de largo plazo. Comparabien muestra tasas y condiciones de aporte.", "inputs": ["balance", "anos", "currency", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "PAGO_MENSUAL", "MINIMO_AP", "PLAZO_MIN", "PLAZO_MAX", "FSD", "UPDATE_DT"], "tips": ["Revisa el aporte mensual que implica tu meta.", "Compara TEA y plazos mínimos/máximos.", "Confirma si el producto tiene respaldo del fondo de depósitos."]},
    {"country": "pe", "slug": "ahorros", "file": "cuentas-de-ahorro.html", "title": "Cuentas de ahorro", "category": "Ahorros", "path": "/cuentas-de-ahorro", "blurb": "TEA, costos y operaciones de cuentas de ahorro.", "summary": "Una cuenta de ahorro guarda tu dinero con disponibilidad y una tasa. Comparabien contrasta TEA, costos y canales de operación.", "inputs": ["balance", "currency", "type", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "MAIN_COST", "MINIMO_AP", "ONLINE", "OP_ATM", "OP_VENTANILLA", "FSD", "UPDATE_DT"], "tips": ["Si usas mucho la cuenta, mira costos y canales (ATM/app).", "Una TEA atractiva puede compensar un costo de mantenimiento.", "Verifica el monto mínimo de apertura."]},
    {"country": "pe", "slug": "cuentas-sueldo", "file": "cuentas-sueldo.html", "title": "Cuentas sueldo", "category": "Ahorros", "path": "/cuentas-sueldo", "blurb": "Cuentas para recibir planilla: tasa, costos y beneficios.", "summary": "La cuenta sueldo está pensada para recibir tu remuneración. Comparabien muestra tasa, costos y beneficios asociados.", "inputs": ["balance", "currency", "type", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "MAIN_COST", "MINIMO_AP", "BENEFITS", "ONLINE", "OP_ATM", "FSD", "UPDATE_DT"], "tips": ["Prioriza beneficios que uses con tu sueldo (descuentos, sin comisiones).", "Compara costos de mantenimiento y facilidad digital.", "Revisa si hay requisitos de abono de planilla."]},
    {"country": "pe", "slug": "cts", "file": "cts.html", "title": "CTS", "category": "Ahorros", "path": "/cts", "blurb": "Cuentas CTS: TEA, traslados y condiciones de operación.", "summary": "La CTS es un beneficio laboral que puedes depositar en una entidad. Comparabien compara tasas y condiciones de traslado u operación.", "inputs": ["balance", "currency", "type", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "MAIN_COST", "MINIMO_AP", "TRAS_PRE", "TRAS_SUE", "OP_ATM", "FSD", "UPDATE_DT"], "tips": ["Si vas a trasladar tu CTS, revisa condiciones de traslado.", "Compara TEA neta de costos.", "Confirma canales para consultar o disponer según reglas vigentes."]},
    {"country": "pe", "slug": "afp", "file": "afp.html", "title": "AFP", "category": "Inversiones", "path": "/afp", "blurb": "Comisiones y rentabilidades de fondos de pensiones AFP.", "summary": "Las AFP administran tus fondos de pensiones. Comparabien te ayuda a contrastar comisiones y rentabilidades históricas por tipo de fondo.", "inputs": ["tipofondo", "balance", "metodo", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TYPE", "COM_REM", "COM_SA_MIX", "RENT_1", "RENT_3", "RENT_5", "RENT_10", "UPDATE_DT"], "tips": ["Compara comisión y rentabilidad juntas, no por separado.", "El tipo de fondo debe alinearse con tu horizonte y tolerancia al riesgo.", "Rentabilidades pasadas no garantizan resultados futuros."]},
    {"country": "pe", "slug": "fondos-mutuos", "file": "fondos-mutuos.html", "title": "Fondos mutuos", "category": "Inversiones", "path": "/fondos-mutuos", "blurb": "Rentabilidad, tipo de fondo y monto mínimo de inversión.", "summary": "Un fondo mutuo agrupa aportes para invertir en un portafolio. Comparabien muestra rentabilidades y mínimos de apertura por tipo de fondo.", "inputs": ["type", "balance", "currency", "days", "years", "pension"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TYPE", "OPEN_MIN", "RENT_1", "RENT_3", "RENT_5", "RENT_M", "GANANCIA", "UPDATE_DT"], "tips": ["Elige el tipo de fondo según tu plazo y riesgo.", "Revisa el mínimo de apertura antes de enamorte de la rentabilidad.", "Compara ventanas de 1, 3 y 5 años para ver consistencia."]},
    {"country": "pe", "slug": "fondos-colectivos", "file": "fondos-colectivos.html", "title": "Fondos colectivos", "category": "Préstamos", "path": "/fondos-colectivos", "blurb": "Consorcios/fondos colectivos: cuota, plazo y costo total.", "summary": "Los fondos colectivos (consorcios) agrupan aportes para adjudicar un bien o crédito. Comparabien compara cuotas, plazos y costos de administración.", "inputs": ["monto", "monto1", "currency", "type", "brand", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "VALOR_CERTIFICADO", "CUOTA_MENSUAL", "PLAZO", "TASA_ADMIN", "PORC_INSCRIPCION", "COSTO_TOTAL", "UPDATE_DT"], "tips": ["Mira el costo total y la tasa de administración, no solo la cuota.", "El plazo y la inscripción cambian mucho el costo efectivo.", "Entiende cómo funciona la adjudicación antes de firmar."]},
    # CO
    {"country": "co", "slug": "soat", "file": "soat.html", "title": "SOAT", "category": "Seguros", "path": "/soat", "blurb": "SOAT en Colombia: precio, cobertura y beneficios.", "summary": "El SOAT es obligatorio para circular. Comparabien compara precios y beneficios entre aseguradoras en Colombia.", "inputs": ["tipo", "geo", "brand", "model", "year"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PRICE", "PRIMA", "COBERTURA", "BENEFITS", "DESCR", "RUNT", "UPDATE_DT"], "tips": ["Compara precio y claridad de cobertura.", "Revisa beneficios extras solo si realmente los usarás.", "Ten a mano los datos del vehículo."]},
    {"country": "co", "slug": "tarjetas-credito", "file": "tarjetas-credito.html", "title": "Tarjetas de crédito", "category": "Tarjetas", "path": "/tarjetas-de-credito", "blurb": "Cuota de manejo, tasas y beneficios de tarjetas.", "summary": "Compara tarjetas en Colombia por cuota de manejo, tasas e ingreso mínimo según tu perfil.", "inputs": ["salary", "brand", "bonus"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "BRAND", "ANNUAL_COST", "MONTH_COST", "SALARIO_MIN", "TEA_MIN", "TEA_MAX", "BONUS", "UPDATE_DT"], "tips": ["Cuota de manejo + tasa importan juntas.", "Elige beneficios que uses de verdad.", "Verifica el ingreso mínimo."]},
    {"country": "co", "slug": "creditos-consumo", "file": "creditos-consumo.html", "title": "Créditos de consumo", "category": "Créditos", "path": "/creditos-de-consumo", "blurb": "Cuota y tasas de créditos de consumo / libre inversión.", "summary": "Los créditos de consumo financian gastos personales. Comparabien estima cuota y tasas según monto, plazo e ingreso.", "inputs": ["monto", "meses", "salary", "currency", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "INS_COST", "PAGO_TOTAL", "UPDATE_DT"], "tips": ["Compara cuota y costo total del crédito.", "Revisa seguros asociados al préstamo.", "Ajusta plazo para equilibrar cuota vs. intereses."]},
    {"country": "co", "slug": "creditos-vehiculos", "file": "creditos-vehiculos.html", "title": "Créditos de vehículos", "category": "Créditos", "path": "/creditos-de-vehiculos", "blurb": "Financiación de vehículos: cuota, tasas y seguros.", "summary": "Financia tu vehículo comparando cuotas, tasas y seguros asociados en Colombia.", "inputs": ["monto", "meses", "salary", "currency", "auto", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "INS_AUTO", "PAGO_TOTAL", "UPDATE_DT"], "tips": ["Incluye el seguro del vehículo en el costo.", "Plazos largos bajan cuota y suben intereses.", "Confirma requisitos de ingreso."]},
    {"country": "co", "slug": "creditos-vivienda", "file": "creditos-vivienda.html", "title": "Créditos hipotecarios", "category": "Créditos", "path": "/creditos-hipotecarios", "blurb": "Vivienda: cuota, TEA/TCEA y seguros.", "summary": "Compara créditos de vivienda en Colombia por cuota, tasas y costos de seguros ligados al inmueble.", "inputs": ["monto", "anos", "salary", "currency", "casa", "type", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "TCEA", "FINANCE", "INS_HOUSE", "UPDATE_DT"], "tips": ["Revisa TCEA para ver el costo más completo.", "Seguro de inmueble y vida suelen sumar a la cuota.", "Compara el porcentaje realmente financiado."]},
    {"country": "co", "slug": "prestamos-rapidos", "file": "prestamos-rapidos.html", "title": "Préstamos rápidos", "category": "Créditos", "path": "/prestamos-rapidos", "blurb": "Créditos de corto plazo: costo y velocidad.", "summary": "Préstamos de desembolso ágil. Comparabien muestra pago, intereses y tiempo de aprobación.", "inputs": ["monto", "dias", "type"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PAGO", "INT_DIARIO", "CAT", "TIEMPO_APROBACION", "UPDATE_DT"], "tips": ["Úsalos con plazos muy cortos.", "Compara el pago total.", "Velocidad no debería opacar el costo."]},
    {"country": "co", "slug": "seguros-carros", "file": "seguros-carros.html", "title": "Seguros de carros", "category": "Seguros", "path": "/seguros-de-carros", "blurb": "Prima, coberturas y deducibles del seguro de carro.", "summary": "Compara seguros de carro en Colombia por prima, coberturas y deducibles según tu vehículo.", "inputs": ["brand", "model", "year", "geo", "cover", "price"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PRIMA", "CUOTA", "COVER", "TEM", "UPDATE_DT"], "tips": ["Revisa deducibles además de la prima.", "Define la cobertura que realmente necesitas.", "Ten listos los datos del vehículo."]},
    {"country": "co", "slug": "cdt", "file": "cdt.html", "title": "CDT", "category": "Ahorros", "path": "/cdt", "blurb": "Certificados de depósito a término: tasa y ganancia.", "summary": "Un CDT fija tu dinero por un plazo a cambio de una tasa. Comparabien estima ganancia según monto y días.", "inputs": ["balance", "days", "currency", "estado"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "GANANCIA_TOTAL", "MINIMO_AP", "PLAZO_MIN", "PLAZO_MAX", "UPDATE_DT"], "tips": ["Compara tasa y ganancia para tu plazo exacto.", "Revisa el monto mínimo.", "Evalúa liquidez: el dinero queda inmovilizado hasta el vencimiento."]},
    {"country": "co", "slug": "ahorros", "file": "cuentas-de-ahorro.html", "title": "Cuentas de ahorro", "category": "Ahorros", "path": "/cuentas-de-ahorro", "blurb": "Cuentas de ahorro: tasa y costos.", "summary": "Compara cuentas de ahorro en Colombia por tasa, costos y monto mínimo.", "inputs": ["balance", "currency", "type"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "MAIN_COST", "MINIMO_AP", "UPDATE_DT"], "tips": ["Mira tasa y costo de manejo juntos.", "Verifica el mínimo de apertura.", "Elige según cuánto usas la cuenta día a día."]},
    {"country": "co", "slug": "fondos-pensiones", "file": "fondos-pensiones.html", "title": "Fondos de pensiones", "category": "Inversiones", "path": "/fondos-de-pensiones", "blurb": "Rentabilidades de fondos de pensiones.", "summary": "Compara fondos de pensiones por tipo y rentabilidades referenciales en distintos horizontes.", "inputs": ["type", "balance"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TYPE", "RENT_1", "RENT_3", "RENT_5", "RENT_10", "GANANCIA", "UPDATE_DT"], "tips": ["Alinea el tipo de fondo con tu horizonte.", "Compara varias ventanas de rentabilidad.", "Rentabilidad pasada no garantiza resultados futuros."]},
    {"country": "co", "slug": "fondos-inversion", "file": "fondos-inversion.html", "title": "Fondos de inversión", "category": "Inversiones", "path": "/fondos-de-inversion", "blurb": "Fondos de inversión: rentabilidad y monto mínimo.", "summary": "Compara fondos de inversión colectivos por rentabilidad, tipo y monto mínimo de apertura.", "inputs": ["type", "balance", "currency"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TYPE", "OPEN_MIN", "RENT_1", "RENT_3", "RENT_5", "GANANCIA", "UPDATE_DT"], "tips": ["Revisa el mínimo de apertura.", "El tipo de fondo define el riesgo.", "Compara horizontes de 1, 3 y 5 años."]},
    # BR
    {"country": "br", "slug": "cartoes-credito", "file": "cartoes-credito.html", "title": "Cartões de crédito", "category": "Cartões", "path": "/cartoes-de-credito", "blurb": "Anuidade, taxas e benefícios de cartões.", "summary": "Compare cartões de crédito no Brasil por anuidade, taxas, renda mínima e benefícios.", "inputs": ["salary", "brand", "bonus"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "BRAND", "ANNUAL_COST", "SALARIO_MIN", "TEA_MIN", "TEA_MAX", "BENEFITS", "UPDATE_DT"], "tips": ["Compare anuidade e taxa juntas.", "Escolha benefícios que você realmente usa.", "Confira a renda mínima."], "lang_pack": "pt"},
    {"country": "br", "slug": "emprestimos-pessoais", "file": "emprestimos-pessoais.html", "title": "Empréstimos pessoais", "category": "Financiamento", "path": "/emprestimos-pessoais", "blurb": "Parcelas e taxas de empréstimos pessoais.", "summary": "Compare empréstimos pessoais por valor, prazo, parcela e taxas efetivas.", "inputs": ["monto", "meses", "salary", "currency", "estado", "type", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "TEM_MIN", "TEM_MAX", "PAGO_TOT", "UPDATE_DT"], "tips": ["Defina valor e prazo antes de comparar.", "Olhe parcela e custo total.", "Taxa menor pode ter seguros ou tarifas extras."], "lang_pack": "pt"},
    {"country": "br", "slug": "emprestimos-online", "file": "emprestimos-online.html", "title": "Empréstimos online", "category": "Financiamento", "path": "/emprestimos-online", "blurb": "Crédito rápido online: parcela e taxas.", "summary": "Empréstimos com solicitação digital. Compare parcelas e taxas para valores e prazos curtos ou médios.", "inputs": ["monto", "meses", "salary", "cep", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "TEM_MIN", "TEM_MAX", "PAGO_TOT", "UPDATE_DT"], "tips": ["Use para necessidades pontuais.", "Compare o pagamento total.", "Verifique condições de desembolso."], "lang_pack": "pt"},
    {"country": "br", "slug": "financiamento-veiculos", "file": "financiamento-veiculos.html", "title": "Financiamento de veículos", "category": "Financiamento", "path": "/financiamento-de-veiculos", "blurb": "Parcelas, taxas e seguros do financiamento automotivo.", "summary": "Compare financiamentos de veículos por entrada, prazo, parcela e taxas.", "inputs": ["monto", "meses", "salary", "inicial", "auto", "currency", "estado", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "INS_AUTO", "PAGO_TOT", "UPDATE_DT"], "tips": ["Inclua seguro do veículo no custo.", "Entrada maior reduz juros totais.", "Compare CET/taxa efetiva quando disponível."], "lang_pack": "pt"},
    {"country": "br", "slug": "financiamento-imobiliario", "file": "financiamento-imobiliario.html", "title": "Financiamento imobiliário", "category": "Financiamento", "path": "/financiamento-imobiliario", "blurb": "Casa própria: parcela, CET e seguros.", "summary": "Compare financiamentos imobiliários por valor, prazo, parcela e custo efetivo total.", "inputs": ["monto", "anos", "salary", "casa", "currency", "estado", "type"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA", "CET", "FINANCE", "INS_HOUSE", "UPDATE_DT"], "tips": ["Olhe CET para ver o custo mais completo.", "Seguros do imóvel entram no custo mensal.", "Compare o percentual financiado."], "lang_pack": "pt"},
    {"country": "br", "slug": "contas-correntes", "file": "contas-correntes.html", "title": "Contas correntes", "category": "Contas", "path": "/contas-correntes", "blurb": "Contas correntes: serviços e benefícios.", "summary": "Compare contas correntes pelos serviços inclusos e benefícios do pacote.", "inputs": ["type", "balance"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "SERVICES", "BENEFITS", "UPDATE_DT"], "tips": ["Escolha pelos serviços que você usa.", "Pacotes 'grátis' podem ter requisitos de movimentação.", "Compare canais digitais e atendimento."], "lang_pack": "pt"},
    {"country": "br", "slug": "cdb", "file": "cdb.html", "title": "CDB", "category": "Contas", "path": "/cdb", "blurb": "CDB: taxa, prazo e rendimento estimado.", "summary": "Compare CDBs por valor aplicado, prazo e rendimento estimado.", "inputs": ["balance", "days", "currency"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "GANANCIA_TOTAL", "MINIMO_AP", "PLAZO_MIN", "PLAZO_MAX", "UPDATE_DT"], "tips": ["Compare rendimento no seu prazo.", "Veja o valor mínimo de aplicação.", "Considere liquidez até o vencimento."], "lang_pack": "pt"},
    {"country": "br", "slug": "planos-saude", "file": "planos-saude.html", "title": "Planos de saúde", "category": "Saúde", "path": "/planos-de-saude", "blurb": "Mensalidade, rede hospitalar e coberturas.", "summary": "Compare planos de saúde por preço, hospitais, abrangência e tipo de acomodação.", "inputs": ["cantidad", "estado", "municipio", "cep", "cover", "acomoda", "copart", "geotip", "choice", "clinicas"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PRIMA", "HOSPITAIS", "GEO_COVERAGE", "ROOM_TYPE", "COPART", "COVERAGES", "UPDATE_DT"], "tips": ["Comece pela rede hospitalar da sua cidade.", "Mensalidade baixa pode limitar acomodação ou cobertura.", "Confira abrangência geográfica e coparticipação."], "lang_pack": "pt"},
    {"country": "br", "slug": "consorcios-imoveis", "file": "consorcios-imoveis.html", "title": "Consórcios de imóveis", "category": "Financiamento", "path": "/consorcios-imoveis", "blurb": "Consórcio imobiliário: parcelas, prazos e custos.", "summary": "Compare consórcios de imóveis por valor, parcelas, prazo e taxas administrativas.", "inputs": ["monto", "meses", "currency", "estado"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "MONTO", "CUOTA1", "MES_TOT", "ADM_COST", "COSTO_TOT", "CET", "UPDATE_DT"], "tips": ["Entenda como funciona a contemplação.", "Compare taxa de administração e custo total.", "Parcela inicial pode diferir das demais."], "lang_pack": "pt"},
    {"country": "br", "slug": "seguros-carros", "file": "seguros-carros.html", "title": "Seguros de carros", "category": "Seguros", "path": "/seguros-de-carros", "blurb": "Seguro auto: preço e coberturas essenciais.", "summary": "Compare seguros de carro no Brasil com foco em preço, perfil do veículo e coberturas principais.", "inputs": ["brand", "geo", "model", "year", "cover"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PRIMA", "COVER", "BENEFITS", "UPDATE_DT"], "tips": ["Não compare só o preço: veja franquia e coberturas.", "Tenha marca, modelo e ano em mãos.", "Assistência 24h e vidros costumam diferenciar planos."], "lang_pack": "pt"},
    # MX
    {"country": "mx", "slug": "tarjetas-credito", "file": "tarjetas-credito.html", "title": "Tarjetas de crédito", "category": "Tarjetas", "path": "/tarjetas-de-credito", "blurb": "Anualidad, tasas y beneficios de tarjetas.", "summary": "Compara tarjetas en México por anualidad, tasa, ingreso mínimo y beneficios.", "inputs": ["salary", "brand", "bonus", "estado", "type"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "BRAND", "ANNUAL_COST", "MONTH_COST", "SALARIO_MIN", "TEA_MN", "BONUS", "UPDATE_DT"], "tips": ["Anualidad y CAT/tasa importan juntas.", "Elige beneficios que sí uses.", "Verifica el ingreso mínimo."]},
    {"country": "mx", "slug": "prestamos-personales", "file": "prestamos-personales.html", "title": "Préstamos personales", "category": "Créditos", "path": "/prestamos-personales", "blurb": "Monto, plazo, cuota y tasas de préstamos.", "summary": "Compara préstamos personales en México por cuota, tasas y costos iniciales.", "inputs": ["monto", "meses", "salary", "currency", "estado", "type", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "INITIAL_COST", "PAGO_TOTAL", "UPDATE_DT"], "tips": ["Compara cuota y pago total.", "Revisa costos de apertura.", "Ajusta el plazo para equilibrar cuota e intereses."]},
    {"country": "mx", "slug": "prestamos-inmediatos", "file": "prestamos-inmediatos.html", "title": "Préstamos inmediatos", "category": "Créditos", "path": "/prestamos-inmediatos", "blurb": "Crédito rápido: CAT, interés diario y aprobación.", "summary": "Préstamos de respuesta ágil. Comparabien muestra CAT, pago y tiempo de aprobación.", "inputs": ["monto", "dias", "salary", "currency", "estado", "type"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PAGO", "CAT", "INT_DIARIO", "COMISION", "TIEMPO_APROBACION", "UPDATE_DT"], "tips": ["Úsalos solo a muy corto plazo.", "El CAT resume mejor el costo.", "Velocidad no sustituye comparar el pago total."]},
    {"country": "mx", "slug": "creditos-hipotecarios", "file": "creditos-hipotecarios.html", "title": "Créditos hipotecarios", "category": "Créditos", "path": "/creditos-hipotecarios", "blurb": "Hipotecas: cuota, tasas y seguros.", "summary": "Compara créditos hipotecarios por monto, plazo, cuota y costos asociados a la vivienda.", "inputs": ["monto", "anos", "salary", "casa", "currency", "estado", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "TCEA", "FINANCE", "INS_HOUSE", "UPDATE_DT"], "tips": ["Revisa seguros ligados a la hipoteca.", "Compara el porcentaje financiado.", "Mira el costo total, no solo la tasa."]},
    {"country": "mx", "slug": "creditos-auto", "file": "creditos-auto.html", "title": "Créditos automotrices", "category": "Créditos", "path": "/creditos-automotrices", "blurb": "Financiamiento de auto: cuota y tasas.", "summary": "Compara créditos automotrices por monto, plazo, cuota y seguros del vehículo.", "inputs": ["monto", "meses", "salary", "auto", "currency", "estado", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "INS_AUTO", "PAGO_TOTAL", "UPDATE_DT"], "tips": ["Incluye seguro del auto en el costo.", "Plazo largo baja cuota y sube intereses.", "Confirma requisitos de ingreso."]},
    {"country": "mx", "slug": "inversiones-plazo", "file": "inversiones-plazo.html", "title": "Inversiones a plazo", "category": "Ahorros", "path": "/inversiones-a-plazo", "blurb": "Inversión a plazo: tasa y ganancia estimada.", "summary": "Compara inversiones a plazo fijo por monto, días y ganancia estimada.", "inputs": ["balance", "days", "currency", "estado", "type"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "GANANCIA_TOTAL", "MINIMO_AP", "PLAZO_MIN", "PLAZO_MAX", "UPDATE_DT"], "tips": ["Compara ganancia en tu plazo exacto.", "Revisa el monto mínimo.", "Considera que el dinero queda invertido hasta el vencimiento."]},
    {"country": "mx", "slug": "ahorros", "file": "cuentas-de-ahorro.html", "title": "Cuentas de ahorro", "category": "Ahorros", "path": "/cuentas-de-ahorro", "blurb": "Cuentas de ahorro: tasa y costos.", "summary": "Compara cuentas de ahorro en México por tasa, costos y monto mínimo.", "inputs": ["balance", "currency", "estado", "type"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TEA", "MAIN_COST", "MINIMO_AP", "UPDATE_DT"], "tips": ["Tasa y comisiones importan juntas.", "Verifica el mínimo de apertura.", "Elige según el uso diario de la cuenta."]},
    {"country": "mx", "slug": "afores", "file": "afores.html", "title": "Afores", "category": "Inversiones", "path": "/afores", "blurb": "Afores: comisiones y rendimientos.", "summary": "Compara Afores por comisión, IRN y rendimientos en distintos horizontes.", "inputs": ["edad", "balance", "tipo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "COMISION", "IRN", "REND_12", "REND_24", "REND_36", "REND_5A", "UPDATE_DT"], "tips": ["Comisión baja + buen rendimiento suele ser el equilibrio.", "Revisa horizontes de 12 a 60 meses.", "Rendimientos pasados no garantizan el futuro."]},
    {"country": "mx", "slug": "seguros-auto", "file": "seguros-auto.html", "title": "Seguros de auto", "category": "Seguros", "path": "/seguros-de-auto", "blurb": "Seguro de auto: precio y coberturas clave.", "summary": "Compara seguros de auto en México con foco en prima, perfil del vehículo y coberturas principales.", "inputs": ["brand", "geo", "model", "year", "cover"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PRIMA", "COVER", "BENEFITS", "UPDATE_DT"], "tips": ["Compara deducible y coberturas, no solo precio.", "Ten listos marca, modelo y año.", "Asistencias y cobertura amplia marcan diferencias."]},
    # ES
    {"country": "es", "slug": "tarjetas-credito", "file": "tarjetas-credito.html", "title": "Tarjetas de crédito", "category": "Tarjetas", "path": "/tarjetas-de-credito", "blurb": "Cuota anual, TAE/TIN y beneficios.", "summary": "Compara tarjetas en España por cuota, TAE/TIN, ingreso mínimo y beneficios.", "inputs": ["salary", "brand", "bonus", "credit", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "BRAND", "ANNUAL_COST", "MONTH_COST", "SALARIO_MIN", "TAE", "TIN", "BONUS", "UPDATE_DT"], "tips": ["Compara cuota anual y TAE juntas.", "Elige beneficios que uses.", "Revisa el tipo de tarjeta (crédito/débito diferido)."]},
    {"country": "es", "slug": "prestamos-personales", "file": "prestamos-personales.html", "title": "Préstamos personales", "category": "Préstamos", "path": "/prestamos-personales", "blurb": "Cuota, TAE y coste total del préstamo.", "summary": "Compara préstamos personales por importe, plazo, cuota y tipos de interés.", "inputs": ["monto", "meses", "salary", "currency", "geo", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TEA_MIN", "TEA_MAX", "TN_MIN", "TN_MAX", "PAGO_TOTAL", "UPDATE_DT"], "tips": ["Compara cuota y coste total.", "Revisa comisiones de apertura.", "Ajusta el plazo para equilibrar cuota e intereses."]},
    {"country": "es", "slug": "prestamos-rapidos", "file": "prestamos-rapidos.html", "title": "Préstamos rápidos", "category": "Préstamos", "path": "/prestamos-rapidos", "blurb": "Microcréditos: coste y velocidad de aprobación.", "summary": "Préstamos de respuesta rápida. Comparabien muestra pago, interés diario y tiempo de aprobación.", "inputs": ["monto", "dias", "salary", "currency", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "PAGO", "INT_DIARIO", "COMISION", "CAT", "TIEMPO_APROBACION", "UPDATE_DT"], "tips": ["Solo para necesidades muy urgentes y cortas.", "Compara el pago total.", "La velocidad no debe ocultar el coste."]},
    {"country": "es", "slug": "prestamos-coches", "file": "prestamos-coches.html", "title": "Préstamos para coches", "category": "Préstamos", "path": "/prestamos-para-coches", "blurb": "Financiación de coche: cuota, TIN y TAE.", "summary": "Compara préstamos para coches por importe, entrada, plazo y tipos de interés.", "inputs": ["monto", "meses", "salary", "inicial", "auto", "currency", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TIN", "TAE", "COMISION", "PAGO_TOT", "UPDATE_DT"], "tips": ["Mira TAE para comparar el coste real.", "Una entrada mayor suele mejorar condiciones.", "Revisa comisiones adicionales."]},
    {"country": "es", "slug": "hipotecas", "file": "hipotecas.html", "title": "Hipotecas", "category": "Hipotecas", "path": "/hipotecas", "blurb": "Hipotecas: cuota, TIN/TAE y Euríbor.", "summary": "Compara hipotecas en España por importe, plazo, cuota y tipo de interés (fijo/variable).", "inputs": ["monto", "anos", "salary", "casa", "inicial", "currency", "geo", "minmax"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "CUOTA", "TIN", "TEA", "EURIBOR", "INI_COST", "TIPO", "UPDATE_DT"], "tips": ["Compara TIN y TAE; la TAE incluye más costes.", "En variables, entiende el Euríbor + diferencial.", "Revisa gastos iniciales de constitución."]},
    {"country": "es", "slug": "cuentas", "file": "cuentas.html", "title": "Cuentas", "category": "Ahorros", "path": "/cuentas", "blurb": "Cuentas: remuneración, TIN/TEA y comisiones.", "summary": "Compara cuentas en España por remuneración, comisiones y saldo mínimo.", "inputs": ["balance", "currency", "type", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TIN", "TEA", "MAIN_COST", "MINIMO_AP", "UPDATE_DT"], "tips": ["Remuneración y comisiones van juntas.", "Revisa requisitos de nómina o domiciliaciones.", "Confirma el saldo mínimo."]},
    {"country": "es", "slug": "depositos", "file": "depositos.html", "title": "Depósitos", "category": "Ahorros", "path": "/depositos", "blurb": "Depósitos a plazo: TIN/TEA y ganancia.", "summary": "Compara depósitos a plazo por importe, meses y rentabilidad estimada.", "inputs": ["balance", "meses", "currency", "type", "geo"], "outputs": ["COMPANY_NAME", "PRODUCT_NAME", "TIN", "TEA", "GANANCIA_TOTAL", "MINIMO_AP", "PLAZO_MIN", "PLAZO_MAX", "UPDATE_DT"], "tips": ["Compara rentabilidad en tu plazo exacto.", "Revisa el mínimo de constitución.", "El capital suele quedar inmovilizado hasta vencimiento."]},
]


COPY = {
    "es": {
        "wiki": "Wiki",
        "nav_countries": "Países",
        "nav_concepts": "Conceptos",
        "compare_now": "Comparar ahora",
        "other_countries": "Otros países",
        "in_this_country": "En este país",
        "all_concepts": "Todos los conceptos",
        "what_compares": "Qué compara {brand}",
        "your_inputs": "Datos que defines tú",
        "your_inputs_intro": "Estos conceptos describen tu situación. Cambiarlos suele cambiar el resultado.",
        "results": "Qué ves en cada resultado",
        "results_intro": "Cada oferta del comparador resume estos conceptos clave:",
        "how_to": "Cómo usarlo en la práctica",
        "cta_compare": "Comparar {title}",
        "cta_home": "Ir a {brand} {country}",
        "note": "Esta página es un glosario de conceptos. No publica código, fórmulas internas ni detalles de implementación del comparador.",
        "concept": "Concepto",
        "means": "Qué significa",
        "look": "Qué mirar",
        "footer": "© Comparabien · Wiki de conceptos",
        "th_input": ("Concepto", "Qué significa"),
        "th_output": ("Concepto", "Qué mirar"),
    },
    "pt": {
        "wiki": "Wiki",
        "nav_countries": "Países",
        "nav_concepts": "Conceitos",
        "compare_now": "Comparar agora",
        "other_countries": "Outros países",
        "in_this_country": "Neste país",
        "all_concepts": "Todos os conceitos",
        "what_compares": "O que o {brand} compara",
        "your_inputs": "Dados que você informa",
        "your_inputs_intro": "Esses conceitos descrevem a sua situação. Mudá-los costuma mudar o resultado.",
        "results": "O que você vê em cada resultado",
        "results_intro": "Cada oferta do comparador resume estes conceitos-chave:",
        "how_to": "Como usar na prática",
        "cta_compare": "Comparar {title}",
        "cta_home": "Ir para {brand} {country}",
        "note": "Esta página é um glossário de conceitos. Não publica código, fórmulas internas nem detalhes de implementação do comparador.",
        "concept": "Conceito",
        "means": "O que significa",
        "look": "O que observar",
        "footer": "© Comparabem · Wiki de conceitos",
        "th_input": ("Conceito", "O que significa"),
        "th_output": ("Conceito", "O que observar"),
    },
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def rows_html(pairs: list[tuple[str, str]], th1: str, th2: str) -> str:
    body = []
    for a, b in pairs:
        body.append(
            f"            <tr>\n              <th scope=\"row\">{esc(a)}</th>\n              <td>{esc(b)}</td>\n            </tr>"
        )
    return f"""        <table class="concept-table">
          <thead>
            <tr>
              <th scope="col">{esc(th1)}</th>
              <th scope="col">{esc(th2)}</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(body)}
          </tbody>
        </table>"""


def page_html(product: dict, siblings: list[dict]) -> str:
    c = COUNTRIES[product["country"]]
    pack = product.get("lang_pack", "pt" if c["lang"].startswith("pt") else "es")
    t = COPY[pack]
    in_labels, out_labels = labels_for(c["lang"])

    compare_url = c["site"] + product["path"]
    inputs = []
    for key in product["inputs"]:
        if key in SKIP_INPUTS:
            continue
        label, meaning = in_labels.get(key, (key.replace("_", " ").title(), "Dato usado para personalizar la comparación." if pack == "es" else "Dado usado para personalizar a comparação."))
        inputs.append((label, meaning))

    outputs = []
    for key in pick_outputs(product["outputs"]):
        label, meaning = out_labels.get(key, (key.replace("_", " ").title(), "Indicador mostrado en el resultado." if pack == "es" else "Indicador exibido no resultado."))
        outputs.append((label, meaning))

    tips = "\n".join(f"          <li>{esc(tip)}</li>" for tip in product["tips"])
    local_links = []
    for s in siblings:
        if s["file"] == product["file"]:
            continue
        local_links.append(f'            <li><a href="{esc(s["file"])}">{esc(s["title"])}</a></li>')
        if len(local_links) >= 8:
            break
    side_local = "\n".join(local_links)

    other_countries = []
    for code, meta in COUNTRIES.items():
        if code == product["country"]:
            continue
        other_countries.append(
            f'            <li><a href="{esc(meta["site"])}/" rel="noopener noreferrer">{esc(meta["name"])}</a></li>'
        )

    title_doc = f'{product["title"]} en {c["name"]} | Conceptos Comparabien Wiki' if pack == "es" else f'{product["title"]} no {c["name"]} | Conceitos Comparabem Wiki'
    desc = product["blurb"]

    return f"""<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title_doc)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,550;9..144,650&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="../index.html">
        <img class="brand-mark" src="../assets/comparabien-app.png" width="48" height="48" alt="Comparabien">
        <span>comparabien <em>wiki</em></span>
      </a>
      <nav class="nav" aria-label="Principal">
        <a href="../index.html#paises">{t['nav_countries']}</a>
        <a href="../index.html#conceptos">{t['nav_concepts']}</a>
        <a href="{esc(compare_url)}" rel="noopener noreferrer">{esc(t['cta_compare'].format(title=product['title']))}</a>
      </nav>
    </div>
  </header>

  <main class="wrap">
    <header class="page-hero">
      <nav class="crumbs" aria-label="Breadcrumb">
        <a href="../index.html">{t['wiki']}</a>
        <span aria-hidden="true">/</span>
        <a href="index.html">{esc(c['name'])}</a>
        <span aria-hidden="true">/</span>
        <span>{esc(product['title'])}</span>
      </nav>
      <p class="eyebrow">{esc(c['name'])} · {esc(product['category'])}</p>
      <h1>{esc(product['title'])}: {'conceitos para comparar' if pack == 'pt' else 'conceptos para comparar'}</h1>
      <p class="lede">{esc(product['summary'])}</p>
    </header>

    <div class="layout">
      <article class="article">
        <h2>{esc(t['what_compares'].format(brand=c['brand']))}</h2>
        <p>
          {'Ao usar o comparador de' if pack == 'pt' else 'Al usar el comparador de'}
          <a href="{esc(compare_url)}" rel="noopener noreferrer">{esc(product['title'])} {'no' if pack == 'pt' else 'en'} {esc(c['name'])}</a>,
          {'você vê ofertas lado a lado. Informe o que precisa e compare com clareza.' if pack == 'pt' else 'ves ofertas lado a lado. Indica lo que necesitas y compara con claridad.'}
        </p>

        <h2>{t['your_inputs']}</h2>
        <p>{t['your_inputs_intro']}</p>
{rows_html(inputs, *t['th_input'])}

        <h2>{t['results']}</h2>
        <p>{t['results_intro']}</p>
{rows_html(outputs, *t['th_output'])}

        <h2>{t['how_to']}</h2>
        <ul>
{tips}
        </ul>

        <div class="cta">
          <a class="btn" href="{esc(compare_url)}" rel="noopener noreferrer">{esc(t['cta_compare'].format(title=product['title']))}</a>
          <a class="btn btn-ghost" href="{esc(c['site'])}/" rel="noopener noreferrer">{esc(t['cta_home'].format(brand=c['brand'], country=c['name']))}</a>
        </div>
        <p class="note">{t['note']}</p>
      </article>

      <aside>
        <div class="side-card">
          <h3>{t['compare_now']}</h3>
          <ul>
            <li><a href="{esc(compare_url)}" rel="noopener noreferrer">{esc(product['title'])} · {esc(c['name'])}</a></li>
            <li><a href="{esc(c['site'])}/" rel="noopener noreferrer">{esc(c['site'].replace('https://', ''))}</a></li>
          </ul>
        </div>
        <div class="side-card">
          <h3>{t['in_this_country']}</h3>
          <ul>
{side_local}
          </ul>
        </div>
        <div class="side-card">
          <h3>{t['other_countries']}</h3>
          <ul>
{chr(10).join(other_countries)}
          </ul>
        </div>
        <div class="side-card">
          <h3>{t['wiki']}</h3>
          <ul>
            <li><a href="../index.html">{t['all_concepts']}</a></li>
            <li><a href="index.html">{esc(c['name'])}</a></li>
          </ul>
        </div>
      </aside>
    </div>
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <p>{t['footer']}</p>
      <div class="footer-links">
        <a href="../index.html">{t['wiki']}</a>
        <a href="{esc(compare_url)}" rel="noopener noreferrer">{esc(product['title'])}</a>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def country_index_html(code: str, products: list[dict]) -> str:
    c = COUNTRIES[code]
    pack = "pt" if c["lang"].startswith("pt") else "es"
    cards = []
    for p in products:
        cards.append(
            f"""        <article class="concept-card">
          <div class="meta">
            <span class="chip live">{'Publicado' if pack == 'es' else 'Publicado'}</span>
            <span class="chip">{esc(p['category'])}</span>
          </div>
          <h3><a href="{esc(p['file'])}">{esc(p['title'])}</a></h3>
          <p>{esc(p['blurb'])}</p>
        </article>"""
        )
    title = f"Conceptos · {c['name']} | Comparabien Wiki" if pack == "es" else f"Conceitos · {c['name']} | Comparabem Wiki"
    intro = (
        f"Glosario de conceptos de los comparadores activos de {c['brand']} en {c['name']}."
        if pack == "es"
        else f"Glossário de conceitos dos comparadores ativos do {c['brand']} no {c['name']}."
    )
    return f"""<!DOCTYPE html>
<html lang="{c['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(intro)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,550;9..144,650&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="../index.html">
        <img class="brand-mark" src="../assets/comparabien-app.png" width="48" height="48" alt="Comparabien">
        <span>comparabien <em>wiki</em></span>
      </a>
      <nav class="nav" aria-label="Principal">
        <a href="../index.html#paises">{'Países' if pack == 'es' else 'Países'}</a>
        <a href="../index.html#conceptos">{'Conceptos' if pack == 'es' else 'Conceitos'}</a>
        <a href="{esc(c['site'])}/" rel="noopener noreferrer">{esc(c['brand'])}</a>
      </nav>
    </div>
  </header>
  <main>
    <section class="hero wrap">
      <p class="eyebrow">{esc(c['code'])} · {esc(c['name'])}</p>
      <h1>{'Conceptos' if pack == 'es' else 'Conceitos'} {esc(c['name'])}</h1>
      <p class="lede">{esc(intro)}</p>
      <p style="margin-top:1rem"><a class="btn" href="{esc(c['site'])}/" rel="noopener noreferrer">{'Ir al sitio' if pack == 'es' else 'Ir ao site'} {esc(c['brand'])}</a></p>
    </section>
    <section class="section wrap">
      <div class="concept-grid">
{chr(10).join(cards)}
      </div>
    </section>
  </main>
  <footer class="site-footer">
    <div class="footer-inner">
      <p>{'© Comparabien · Wiki de conceptos' if pack == 'es' else '© Comparabem · Wiki de conceitos'}</p>
      <div class="footer-links">
        <a href="../index.html">Wiki</a>
        <a href="{esc(c['site'])}/" rel="noopener noreferrer">{esc(c['site'].replace('https://',''))}</a>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def main_index_html(by_country: dict[str, list[dict]]) -> str:
    country_cards = []
    for code, meta in COUNTRIES.items():
        n = len(by_country.get(code, []))
        country_cards.append(
            f"""        <article class="country-card">
          <span class="country-code">{meta['code']}</span>
          <h3><a href="{code}/index.html">{esc(meta['name'])}</a></h3>
          <p>{n} conceptos publicados.</p>
          <a class="site-link" href="{esc(meta['site'])}/" rel="noopener noreferrer">{esc(meta['site'].replace('https://',''))} →</a>
        </article>"""
        )

    concept_cards = []
    for code, products in by_country.items():
        meta = COUNTRIES[code]
        for p in products:
            concept_cards.append(
                f"""        <article class="concept-card">
          <div class="meta">
            <span class="chip live">Publicado</span>
            <span class="chip">{esc(meta['name'])}</span>
          </div>
          <h3><a href="{code}/{esc(p['file'])}">{esc(p['title'])}</a></h3>
          <p>{esc(p['blurb'])}</p>
        </article>"""
            )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Comparabien Wiki | Conceptos de comparación financiera</title>
  <meta name="description" content="Glosario público de conceptos que usa Comparabien para comparar productos financieros y seguros en Perú, Colombia, Brasil, México y España.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,550;9..144,650&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <a class="brand" href="index.html" aria-current="page">
        <img class="brand-mark" src="assets/comparabien-app.png" width="48" height="48" alt="Comparabien">
        <span>comparabien <em>wiki</em></span>
      </a>
      <nav class="nav" aria-label="Principal">
        <a href="#paises">Países</a>
        <a href="#conceptos">Conceptos</a>
        <a href="https://comparabien.com.pe/" rel="noopener noreferrer">Comparabien</a>
      </nav>
    </div>
  </header>

  <main>
    <section class="hero wrap">
      <p class="eyebrow">Recurso público · Comparación transparente</p>
      <h1>Wiki de conceptos Comparabien</h1>
      <p class="lede">
        Explicamos, en lenguaje claro, qué significa cada dato que ves al comparar
        préstamos, tarjetas, depósitos y seguros. Sin jerga técnica: solo los
        conceptos que te ayudan a elegir mejor.
      </p>
    </section>

    <section class="section wrap" id="paises">
      <h2>Sitios Comparabien</h2>
      <p class="section-intro">
        Cada país tiene su propio mercado y productos. Entra al sitio local o
        explora los conceptos del wiki.
      </p>
      <div class="country-grid">
{chr(10).join(country_cards)}
      </div>
    </section>

    <section class="section wrap" id="conceptos">
      <h2>Conceptos publicados</h2>
      <p class="section-intro">
        Cada página corresponde a un comparador activo. Usa los filtros por país
        o explora el catálogo completo.
      </p>
      <div class="concept-grid">
{chr(10).join(concept_cards)}
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <p>© Comparabien · Wiki de conceptos (GitHub Pages)</p>
      <div class="footer-links">
        <a href="https://comparabien.com.pe/" rel="noopener noreferrer">Perú</a>
        <a href="https://comparabien.com.co/" rel="noopener noreferrer">Colombia</a>
        <a href="https://comparabem.com.br/" rel="noopener noreferrer">Brasil</a>
        <a href="https://comparabien.com.mx/" rel="noopener noreferrer">México</a>
        <a href="https://comparabien.es/" rel="noopener noreferrer">España</a>
      </div>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    by_country: dict[str, list[dict]] = {k: [] for k in COUNTRIES}
    for p in PRODUCTS:
        by_country[p["country"]].append(p)

    for code, products in by_country.items():
        out_dir = ROOT / code
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(country_index_html(code, products), encoding="utf-8")
        for p in products:
            html = page_html(p, products)
            (out_dir / p["file"]).write_text(html, encoding="utf-8")

    (ROOT / "index.html").write_text(main_index_html(by_country), encoding="utf-8")

    # README
    lines = [
        "# comparison-wiki",
        "",
        "Public concept wiki for Comparabien comparison products. Hosted on GitHub Pages.",
        "",
        "## Live site",
        "",
        "https://alfredojez.github.io/comparison-wiki/",
        "",
        "## Markets",
        "",
        "| Country | Site | Concepts |",
        "|---------|------|----------|",
    ]
    for code, meta in COUNTRIES.items():
        lines.append(f"| {meta['name']} | {meta['site']}/ | {len(by_country[code])} |")
    lines += [
        "",
        "## Editorial rule",
        "",
        "Public pages describe **concepts** (what the user chooses and what they see). They must not expose private service code, SQL, hashes, or internal field names.",
        "",
        "## Regenerate",
        "",
        "```bash",
        "python3 scripts/generate_pages.py",
        "```",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")

    total = sum(len(v) for v in by_country.values())
    print(f"Generated {total} product pages + {len(by_country)} country indexes + main index")
    for code, products in by_country.items():
        print(f"  {code}: {len(products)}")


if __name__ == "__main__":
    main()
