---
type: domain-analysis
facility: "ISS-MSG"
investigations: [PSI-107, PSI-108]
tags: [nasa/thermofluids, cvb, peclet, pfe-water-mist]
---

# Termofluidos Interfaciales en Microgravedad (CVB y CVB-2)

Aunque no son incendios de cabina, **CVB** y **CVB-2** (*Constrained Vapor Bubble*) estudian transferencia termica interfacial, evaporacion y condensacion en tuberia de cuarzo sin flotabilidad.

---

## 1. Contenido Utiles y Rol Fisico

- **[[PSI-107_CVB]]:** Mapas interferometricos de espesor de pelicula liquida de pentano, temperatura axial y gradiente termico en tubo cerrado en la `ISS-MSG`.
- **[[PSI-108_CVB-2]]:** Extension con distintas cargas calorificas sobre peliculas delgadas liquidas sin conveccion hidrostatica.

---

## 2. Por Que Importan en Nuestro Pipeline

1. **Fisica de Supresion del Extintor PFE (`O3`):**
   - El extintor orbital `PFE` atomiza agua en microgotas de $20\text{–}100\,\mu\text{m}$ que enfrian la superficie mediante alto calor latente de vaporizacion ($2,260\text{ kJ/kg}$). Las leyes de evaporacion sin conveccion de `CVB/CVB-2` explican el intercambio termico interfacial de peliculas liquidas en $0g$.
2. **Validacion del Numero de Peclet ($\text{Pe}$) y Taxonomia Completada (`O1`, `O2`):**
   - Permite que el motor `PCA + K-Means` (`[[M3_PCA_KMeans_TFIDF_TOPSIS]]`) separe limpiamente el **Cluster de Termofluidos e Intercambio Calorico** frente a incendios de solidos, llamas de gotas y llamas gaseosas, cubriendo el **100% de las 24 investigaciones** oficiales de PSI.

---

## 3. Roles y Objetivos

- **Objetivos:** [[O1_Resumen_y_Ranking_PSI]], [[O2_Prediccion_Inflamabilidad_Habitats]], [[O3_Deteccion_Supresion_Gemelo_FSM]].
- **Dominio:** [[Rol_Mecatronica_y_Control]].
