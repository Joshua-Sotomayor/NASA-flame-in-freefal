---
type: psi-investigation
psi_id: PSI-146
acronym: "ACME - Flame Design"
facility: "ISS - CIR"
domain: "Mecatronica y Control"
doi_prefix: "10.60555"
license: "CC0-1.0"
tags: [nasa/psi, combustion, "psi-146"]
---

# PSI-146: ACME - Flame Design

**Instalacion:** `ISS - CIR` | **Dominio / Rol:** [[Rol_Mecatronica_y_Control]] (`Mecatronica y Control`) | **Licencia:** `CC0-1.0` (`10.60555`)

## 1. Que contiene el repositorio PSI / OSDR
Metadatos CIR/ISA-Tab, imagenes opticas OH*/CH* de llamas difusivas esfericas de etileno y metano y series de radiometro.

## 2. Informacion util y variables criticas
Caracteriza llamas esfericas azules simetricas libres de hollin en microgravedad pura manipulando estequiometria y direccion de flujo.

## 3. Como alimenta el entrenamiento ML / DL propio
Entrega la firma optica prototipica de la clase `1: Llama Esferica Azul 0g` para entrenar `flame_cnn.onnx` (`M2`) y texto tecnico de arquitectura en `M3`.

## 4. Conexiones en el Grafo de Conocimiento
- **Modelos ML/DL:** [[M2_CNN_ONNX_DecisionTree_FSM]], [[M3_PCA_KMeans_TFIDF_TOPSIS]]
- **Objetivos del Reto:** [[O1_Resumen_y_Ranking_PSI]], [[O3_Deteccion_Supresion_Gemelo_FSM]]
- **Investigaciones relacionadas:** [[PSI-147_ACME-s-Flame]], [[PSI-153_ACME-CLD-Flame]]
- **Ver tambien:** [[00_MOC_Indice_Maestro_AERO_IGNIS]] | [[01_Objetivos_Dominios_y_Roles]]
