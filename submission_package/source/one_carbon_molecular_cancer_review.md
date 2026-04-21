# Compartmentalized One-Carbon Flux in Cancer: Mechanisms, Immune Control, and Precision Therapeutics

**Review Article**

**Target journal:** *Molecular Cancer*

**Authors:** [Author names and affiliations to be inserted]

**Corresponding author:** [Name, email, postal address]

## Abstract

**Background:** One-carbon (1C) metabolism integrates the folate and methionine cycles to sustain nucleotide synthesis, methylation reactions, and redox homeostasis. Although the pathway was historically viewed through the lens of antifolate chemotherapy, recent work shows that cancer cells exploit 1C metabolism as a compartmentalized flux system rather than a simple linear biosynthetic pathway.

**Main body:** In many tumors, mitochondrial serine catabolism through SHMT2, MTHFD2, and MTHFD1L generates formate that fuels cytosolic purine and thymidylate synthesis, buffers redox stress, and supports phenotypes extending beyond proliferation, including replication stress tolerance, lineage plasticity, and metastasis. This spatial organization creates selective liabilities. PHGDH amplification or overexpression drives serine synthesis addiction in defined cancer states; SHMT-dependent flux supports hypoxic and folate-stressed tumors; MTHFD2 shows a striking oncofetal expression pattern and couples mitochondrial 1C metabolism to immune evasion and mitotic fitness; and MAT2A becomes targetable in methylthioadenosine phosphorylase (MTAP)-deleted cancers through PRMT5-centered synthetic lethality. One-carbon metabolism also shapes the tumor immune microenvironment. Tumor cells compete with lymphocytes for methionine via SLC43A2, depleting S-adenosylmethionine and histone methylation in tumor-infiltrating T cells. Tumor methionine metabolism can drive T-cell exhaustion, whereas tumor-derived MTHFD2 promotes PD-L1 expression. Conversely, formate supplementation can enhance antitumor CD8+ T-cell fitness and improve PD-1 blockade in preclinical models. These mechanistic insights have converged with translational progress: MAT2A inhibitors and MTA-cooperative PRMT5 inhibitors have entered the clinic, while PHGDH-, SHMT-, and MTHFD2-directed programs remain largely preclinical.

**Conclusion:** A useful organizing principle for the field is that 1C metabolism is a programmable, compartmentalized flux network connecting tumor growth, immune suppression, and therapeutic response. Framing the pathway this way clarifies why successful clinical translation will likely depend on biomarker-guided patient selection, rational combinations with antifolates, DNA damage response therapies, or immunotherapy, and pharmacodynamic readouts that capture flux rather than expression alone.

**Keywords:** one-carbon metabolism; folate cycle; methionine cycle; MTHFD2; PHGDH; SHMT2; MAT2A; PRMT5; MTAP deletion; tumor immunometabolism; formate; precision oncology

## Background

One-carbon (1C) metabolism is a distributed biochemical network that transfers folate-bound single-carbon units to support purine and thymidylate synthesis, methionine regeneration, methyl-donor production, and reductive homeostasis [1]. The pathway includes a cytosolic folate cycle, a mitochondrial folate cycle, the methionine cycle, and transsulfuration. Its importance in cancer was recognized long before “cancer metabolism” became a modern field: methotrexate and 5-fluorouracil validated folate-dependent nucleotide synthesis as a therapeutic vulnerability decades ago. What has changed in the past ten years is not the pathway itself, but the level at which it can be resolved. Stable-isotope tracing, metabolomics, CRISPR screens, structural biology, and patient-scale transcriptomic analyses have shown that malignant cells use 1C metabolism in a highly organized and context-dependent manner [1-6].

An especially important advance has been the realization that 1C metabolism is compartmentalized. In many proliferating cells, mitochondrial serine catabolism generates formate that is exported to the cytosol and re-assimilated into folate pools for nucleotide synthesis [4,7]. This spatial separation gives directionality to 1C flux and helps explain why mitochondrial enzymes such as SHMT2 and MTHFD2 are repeatedly overexpressed in cancer and linked to poor outcome [3,5,8]. It also clarifies why simple expression maps are insufficient. What matters clinically is not only whether the pathway is present, but whether flux is routed through specific compartments to support a given tumor state.

This perspective is also reshaping how 1C metabolism is understood in the tumor immune microenvironment (TIME). Cancer cells can deplete methionine, alter S-adenosylmethionine (SAM) availability, accumulate methylthioadenosine (MTA), and modulate extracellular formate, thereby influencing T-cell epigenetic programming, checkpoint expression, and effector fitness [9-14]. In parallel, drug development has accelerated. The clinically most mature branch of the field is the MAT2A-PRMT5 axis in MTAP-deleted tumors, but selective inhibitors of PHGDH, SHMT, and MTHFD2 are also maturing preclinically [15-21].

In this review, we argue that the most useful cancer-centered framework is to treat 1C metabolism as a **compartmentalized flux system**. From that starting point, tumor-intrinsic biology, immune regulation, and therapeutic strategy become easier to unify. We therefore focus on four themes: the architecture of compartmentalized 1C flux; tumor-intrinsic programs sustained by that flux; how 1C metabolism sculpts the TIME; and the biomarker-led therapeutic landscape that is now emerging.

## Main text

### 1. Architecture of compartmentalized one-carbon metabolism in cancer

#### 1.1. The folate cycle is spatially divided, not redundant

At the biochemical level, serine is the dominant 1C donor for proliferating mammalian cells. SHMT1 in the cytosol and SHMT2 in mitochondria transfer the serine hydroxymethyl group to tetrahydrofolate (THF), yielding glycine and 5,10-methylene-THF [1,4]. In the cytosol, MTHFD1 interconverts folate species that are required for thymidylate and purine synthesis. In mitochondria, SHMT2 couples to MTHFD2 or MTHFD2L and MTHFD1L to produce formate, which can exit the organelle and re-enter cytosolic folate metabolism [1,4].

This arrangement is not simply duplicated chemistry in two compartments. Quantitative flux studies showed that loss of the mitochondrial folate pathway can be buffered by reversal of cytosolic 1C flux in some contexts, but that this compensation is incomplete and conditional [4]. Conversely, cancer cells often upregulate mitochondrial 1C genes preferentially, implying that the mitochondrial arm is not merely backup machinery but a specialized engine for high-flux anabolic states [3,5].

#### 1.2. Mitochondrial formate production creates directional flux

MTHFD2 sits at the center of this architecture. Nilsson and colleagues identified mitochondrial 1C metabolism as one of the most consistently upregulated metabolic programs across cancers, with MTHFD2 as a dominant node [3]. MTHFD2 is especially notable because it is expressed during embryogenesis but is low or undetectable in most adult tissues, an oncofetal pattern that immediately raises therapeutic interest [3,8]. In functional studies, MTHFD2 supports proliferation and viability across multiple cancer models [3,8].

The consequences of mitochondrial 1C activity extend beyond simple carbon donation. Fan and colleagues showed that folate metabolism contributes materially to NADPH generation, linking 1C flux to redox control [2]. Ye and colleagues further demonstrated that SHMT2-dependent serine catabolism protects MYC-driven cells from hypoxic stress by sustaining mitochondrial redox balance [6]. Together, these data support a model in which mitochondrial 1C metabolism is both a carbon source and a redox module.

#### 1.3. Formate overflow is a cancer-relevant phenotype

Meiser and colleagues formalized “formate overflow” as a feature of oxidative cancer, showing that elevated formate release is coupled to mitochondrial 1C metabolism and oxidative phosphorylation [7]. This concept matters because it reframes formate from a passive by-product into a readout of pathway state. A high-formate tumor is not simply making nucleotides; it is operating a mitochondrial-cytosolic carbon shuttle that may affect invasion, immune interactions, and drug response. Subsequent work extended this idea by showing that mitochondrial 1C metabolism can remain functionally active even when cytosolic folate metabolism is suppressed, preserving migration and metastatic capacity independent of primary tumor growth [23].

#### 1.4. Methionine and transsulfuration connect 1C flux to methylation and stress tolerance

The methionine cycle converts methionine to SAM through MAT2A in most cancers. SAM then serves as the methyl donor for DNA, RNA, histone, and protein methyltransferases, while S-adenosylhomocysteine (SAH) and homocysteine form the downstream branch point into remethylation or transsulfuration [1,24]. This is the route by which 1C metabolism reaches the epigenome. Maddocks and colleagues showed that serine metabolism supports the methionine cycle and DNA/RNA methylation in cancer cells through de novo ATP synthesis, highlighting the tight coupling between anabolic carbon handling and epigenetic output [24].

The resulting picture is that 1C metabolism is best understood as an integrated axis with three principal outputs: nucleotide supply, methyl-donor availability, and redox buffering. Which of these outputs dominates depends on tumor lineage, genotype, nutrient state, oxygenation, and therapeutic pressure.

![Figure 1. Compartmentalized one-carbon flux in cancer. The figure summarizes the mitochondrial generation of formate from serine, re-assimilation of formate in the cytosol for nucleotide synthesis, and coupling of the folate cycle to the methionine cycle and transsulfuration. Highlighted target nodes are PHGDH, SHMT1/2, MTHFD2 and MAT2A.](/Users/ocm/Downloads/one_carbon_review_assets/figure1_compartmentalized_flux.png)

### 2. Tumor-intrinsic programs sustained by one-carbon flux

#### 2.1. Nucleotide synthesis and replication stress tolerance

The most established tumor-intrinsic function of 1C metabolism is support of purine and thymidylate synthesis. Yet the clinically relevant point is not merely that nucleotide production is needed, but that some tumors use compartmentalized 1C flux to maintain nucleotide sufficiency under stress. Cuthbertson and colleagues showed that pharmacologic targeting of MTHFD2 with the folate-pathway inhibitor TH9619 suppresses acute myeloid leukemia by inducing thymidine depletion and replication stress [18]. This observation is important because it links mitochondrial folate metabolism directly to replication fitness and implies that 1C-targeted therapy may be especially effective in tumors operating close to the threshold of nucleotide insufficiency.

#### 2.2. Redox adaptation under hypoxia and folate stress

Hypoxia and folate stress expose another layer of dependency. In MYC-driven settings, SHMT2 supports survival under hypoxia by maintaining NADPH/NADP+ balance and controlling reactive oxygen species [6]. SHMT2 is also highly expressed in glioblastoma pseudopalisading cells, where it helps cells survive ischemic microenvironments while creating a dependence on glycine clearance [25]. These observations fit a recurring principle: 1C metabolism becomes critical when tumors must preserve biosynthesis without losing redox control.

#### 2.3. Metastatic behavior can be uncoupled from proliferation

One of the most conceptually important recent findings is that mitochondrial 1C metabolism can drive migration and metastasis even when proliferation is restrained. In a breast cancer model, Kiweler and colleagues showed that mitochondria can preserve an autarkic 1C cycle during cytosolic folate blockade and that disabling mitochondrial 1C metabolism reduces pulmonary metastasis without a commensurate effect on primary tumor growth [23]. This study helps explain why folate-targeted therapy may leave some aggressive phenotypes intact and why subcellular targeting could matter therapeutically.

#### 2.4. Epigenetic state, mitosis, and noncanonical functions

The field has also moved beyond strictly metabolic roles. MTHFD2 was previously shown to localize to the nucleus and promote proliferation independently of its canonical mitochondrial context [8]. More recently, nuclear localization of MTHFD2 was found to be required for correct mitotic progression, linking the enzyme to chromosome congression, centromeric methylation, and global methylation homeostasis [26]. In parallel, p53 loss can transcriptionally derepress MTHFD2, thereby enhancing folate metabolism, purine synthesis, and tumor growth [27]. These studies reinforce the idea that 1C enzymes are not just passive metabolic pipes; some appear to sit at the interface of metabolism, chromatin, and genome maintenance.

### 3. One-carbon metabolism in the tumor immune microenvironment

#### 3.1. T cells are acutely dependent on 1C metabolism

Activated lymphocytes require 1C metabolism for proliferation, purine biosynthesis, and methylation-dependent cell-state control. In CD4 T cells, MTHFD2 functions as a metabolic checkpoint that integrates purine pools, mTORC1 signaling, and histone methylation to regulate effector versus regulatory cell fate [28]. Although this work was performed in immune models rather than tumors, it is directly relevant to cancer because it defines why T cells become vulnerable to 1C metabolite scarcity within the TIME.

#### 3.2. Methionine competition directly impairs antitumor T-cell function

Cancer cells can suppress T cells by outcompeting them for methionine. Bian and colleagues showed that tumor SLC43A2 depletes methionine available to CD8+ T cells, lowering intracellular methionine and SAM, reducing H3K79me2, and diminishing STAT5-dependent effector programs [9]. Methionine supplementation partially restored these defects in preclinical models and in samples from patients with colon cancer [9]. This is a particularly strong demonstration that amino acid competition in the TIME has direct epigenetic consequences.

The same axis extends to CD4 T cells. Pandit and colleagues reported that cancer-cell methionine consumption progressively increases PD-1 expression in CD4 T cells through methionine depletion, reduced H3K79me2, lower AMPK expression, and T-cell dysfunction [10]. In hepatocellular carcinoma, tumor methionine metabolism and MAT2A-driven SAM production were also linked to T-cell exhaustion, and genetic interruption of tumor MAT2A reduced both tumorigenesis and T-cell dysfunction in vivo [11]. Taken together, these studies place methionine handling at the center of tumor-immune competition.

#### 3.3. MTHFD2 couples metabolic state to PD-L1 expression

Tumor-intrinsic 1C metabolism also shapes checkpoint biology more directly. Wang and colleagues identified MTHFD2 as a driver of immune evasion through PD-L1 upregulation [12]. Mechanistically, MTHFD2 promoted both basal and interferon-gamma-induced PD-L1 expression and was required for efficient tumorigenesis in vivo, establishing a direct link between the folate cycle and checkpoint ligand abundance [12]. This finding raises the possibility that MTHFD2 inhibition could exert dual effects: suppressing tumor metabolism while simultaneously de-repressing antitumor immunity.

#### 3.4. Formate can act as a beneficial metabolite for reinvigorated CD8 T cells

If methionine competition represents the suppressive side of 1C immunometabolism, formate supplementation illustrates the supportive side. Rowe and colleagues showed that therapeutic formate supplementation enhances antitumor CD8+ T-cell fitness and improves the efficacy of PD-1 blockade in B16-OVA tumors [13]. Combined formate and anti-PD-1 treatment increased tumor-infiltrating CD8+ T cells and improved tumor control. This does not mean that all formate in the tumor ecosystem is beneficial; rather, it shows that 1C metabolite availability can be manipulated to favor T-cell function in selected contexts.

#### 3.5. MTAP loss creates an immunosuppressive metabolite environment

MTAP deletion adds another layer. Gjuka and colleagues demonstrated that MTAP-deficient tumors accumulate MTA intra- and extracellularly, impair T-cell function through PRMT5 inhibition and adenosine receptor agonism, and exhibit resistance to immune checkpoint therapy [14]. Enzymatic depletion of extracellular MTA restored T-cell function and improved antitumor immunity [14]. This is important for two reasons. First, it shows that methionine-cycle disruption can suppress immunity even before a targeted drug is applied. Second, it suggests that MTAP genotype may inform not only tumor-cell targeting but also immunotherapy combinations.

![Figure 2. One-carbon metabolism in the tumor immune microenvironment. Tumor cells suppress T cells by competing for methionine via SLC43A2, by driving MAT2A-dependent methyl-donor metabolism, by accumulating MTA after MTAP loss, and by increasing PD-L1 downstream of MTHFD2. In contrast, formate supplementation can support reinvigorated CD8+ T cells during PD-1 blockade.](/Users/ocm/Downloads/one_carbon_review_assets/figure2_immune_crosstalk.png)

### 4. Therapeutic vulnerabilities across the one-carbon network

#### 4.1. PHGDH: the serine synthesis entry point

PHGDH catalyzes the first committed step of de novo serine synthesis and became a cancer target after two landmark 2011 studies. Possemato and colleagues used functional genomics to show that the serine synthesis pathway is essential in PHGDH-high breast cancer cells [5], whereas Locasale and colleagues demonstrated that PHGDH amplification diverts glycolytic flux into serine biosynthesis and contributes to oncogenesis [29]. Since then, PHGDH has been implicated in additional tumor types and phenotypes, including therapy resistance and metastatic behavior.

Drug discovery has progressed but remains preclinical. CBR-5884 was the first selective small-molecule PHGDH inhibitor to show on-target suppression of serine biosynthesis in cancer cells [16]. NCT-503 broadened the toolkit but also illustrated the challenge of separating on-target metabolic effects from off-target carbon rerouting [30]. More drug-like compounds followed, including BI-4916/BI-4924 and newer medicinal-chemistry series with improved potency and pharmacology [17,31]. At present, however, there are no peer-reviewed clinical efficacy data for selective PHGDH inhibitors in cancer. This gap is important to state clearly, because PHGDH is often described as “clinically advancing” on the basis of pipeline enthusiasm rather than published human evidence.

#### 4.2. SHMT1/2 and related folate enzymes

SHMT enzymes occupy a central branch point because they directly channel serine-derived carbon into folate metabolism. Genetic or pharmacologic SHMT inhibition blocks growth in multiple preclinical models, and in some contexts shows synergy with antifolates [32,33]. The dual SHMT inhibitor SHIN2 demonstrated in vivo target engagement with isotope tracing and improved survival in T-cell acute lymphoblastic leukemia, particularly in combination with methotrexate [32]. Additional chemotypes, including folate-based multitargeted inhibitors such as AGF347, achieved broad-spectrum preclinical antitumor effects [34]. These findings support a rational strategy in which SHMT blockade is used either to deepen folate stress or to exploit glycine-handling liabilities in specific tumors.

#### 4.3. MTHFD2: a selective mitochondrial vulnerability with expanding biology

MTHFD2 remains the emblematic mitochondrial 1C target. Its appeal stems from three convergent features: pan-cancer overexpression, low expression in most adult tissues, and evidence that it supports proliferation, stress tolerance, immune evasion, and mitotic integrity [3,8,12,26]. Several selective inhibitors have now been described, including DS44960156 and newer chemotypes with improved potency and isoform selectivity [19,35]. TH9619 provided strong proof of concept that pharmacologic disruption of MTHFD-dependent flux can cause thymidine depletion and replication stress in AML [18], although the molecule inhibits both MTHFD1 and MTHFD2 catalytic activities and is not a simple mitochondria-restricted probe [18,20].

Despite intense interest, selective MTHFD2 inhibition has not yet generated peer-reviewed clinical efficacy data. For a review aimed at *Molecular Cancer*, that distinction matters. The target is compelling, but the translational story is still preclinical.

#### 4.4. MAT2A and the MTAP-PRMT5 collateral lethality axis

The most clinically advanced branch of 1C-directed therapy exploits MTAP deletion. Kryukov and colleagues and Marjon and colleagues independently showed in 2016 that MTAP deletion creates a dependence on PRMT5 and the MAT2A-PRMT5-RIOK1 axis [15,36]. The underlying logic is elegant: MTAP loss causes MTA accumulation, partially suppressing PRMT5 and sensitizing tumor cells to further perturbation of methylation machinery. Kalev and colleagues later showed that MAT2A inhibition blocks growth of MTAP-deleted cancer cells by reducing PRMT5-dependent RNA splicing and inducing DNA damage, thereby providing a direct pharmacologic route into this vulnerability [37].

This axis has now reached human trials. AG-270/S095033, a first-in-class MAT2A inhibitor, produced pharmacodynamic target engagement and early signs of activity in a phase I trial of advanced malignancies [21]. In parallel, second-generation MTA-cooperative PRMT5 inhibitors have shown the clearest early efficacy signal in the entire OCM field. Published phase I dose-exploration data for AMG 193 reported an objective response rate of 21.4% at active and tolerable doses, with responses across eight tumor types and without clinically significant myelosuppression [38]. MRTX1719 and related agents are also being developed in MTAP-deleted solid tumors and may have favorable immunologic properties because they preferentially inhibit PRMT5 in MTA-rich tumor contexts rather than in immune cells [39].

#### 4.5. Classical antifolates should be revisited, not sidelined

A modern review of 1C metabolism should not separate new targets from old drugs too sharply. Methotrexate, pemetrexed, and fluoropyrimidines remain clinically relevant because they validate the pathway and can create the biochemical context in which newer agents become more effective. Preclinical studies already support combinations such as SHMT inhibition plus methotrexate [32] and MAT2A inhibition plus taxanes [37]. MTAP deficiency also appears to create antifolate sensitivity in some settings, especially where purine synthesis is already constrained [40]. The translational message is that new 1C therapeutics will probably succeed first as rational combinations rather than as broad monotherapies.

### 5. Biomarkers, pharmacodynamics, and precision strategy

#### 5.1. Genotype is necessary but not sufficient

The cleanest biomarker in the field is MTAP homozygous deletion, which directly nominates MAT2A and MTA-cooperative PRMT5 strategies [15,21,37-39]. PHGDH amplification is also biologically meaningful, especially in defined breast cancer and melanoma subsets [5,29]. By contrast, MTHFD2 and SHMT2 are usually stratified by expression rather than genomics. This is useful, but it is less precise than a deletion biomarker and may not fully capture flux state.

#### 5.2. Flux-informed biomarkers are the next step

Because 1C metabolism is dynamic and compartmentalized, static expression measurements are imperfect surrogates. Candidate pharmacodynamic biomarkers include SAM depletion, symmetric dimethylarginine suppression, MTA accumulation, folate-species remodeling, and circulating or intratumoral formate. In early MAT2A and PRMT5 studies, paired biopsies and ctDNA have already provided evidence of pathway engagement [21,38]. Comparable flux-sensitive markers will be important if PHGDH-, SHMT-, or MTHFD2-directed agents enter clinical testing.

#### 5.3. Rational combinations should be matched to pathway logic

Three combination principles appear especially compelling. First, **OCM inhibition plus immunotherapy** is justified when the intervention is expected either to relieve immune suppression in tumor cells or to preserve T-cell fitness, as with MTHFD2- or MTAP-directed strategies [12-14,39]. Second, **OCM inhibition plus antifolates or nucleotide stress** is logical when the aim is to deepen replication stress, as seen with SHMT-methotrexate or MTHFD targeting [18,32]. Third, **OCM inhibition plus DNA damage response or mitotic therapy** is attractive when pathway blockade produces DNA damage, mitotic defects, or splicing stress, as observed for MAT2A inhibition [26,37].

![Figure 3. Therapeutic and biomarker landscape for one-carbon metabolism in cancer. The diagram aligns target class, mechanism, evidence strength, and biomarker strategy. MTAP deletion anchors the most mature clinical branch (MAT2A and MTA-cooperative PRMT5 inhibitors), whereas PHGDH, SHMT, and MTHFD2 programs remain predominantly preclinical and will likely require flux-informed pharmacodynamic markers and rational combinations.](/Users/ocm/Downloads/one_carbon_review_assets/figure3_precision_therapeutics.png)

## Tables

**Table 1. Core one-carbon metabolism nodes and their cancer-relevant outputs**

| Node | Main compartment | Core biochemical role | Principal cancer-relevant output | Representative evidence |
|---|---|---|---|---|
| PHGDH | Cytosol | First committed step of de novo serine synthesis | Serine supply, carbon diversion from glycolysis, context-specific metabolic addiction | PHGDH amplification and dependency in breast cancer and melanoma [5,29] |
| SHMT1/2 | Cytosol / mitochondria | Transfer of serine-derived 1C units to THF | Coupling of serine metabolism to folate flux, glycine balance, nucleotide synthesis | SHMT inhibition blocks tumor growth and synergizes with methotrexate [32,33] |
| MTHFD2 | Mitochondria and, in some contexts, nucleus | Oxidation/cyclohydrolase steps in mitochondrial 1C metabolism | Formate production, redox support, immune evasion, mitotic fitness | Pan-cancer overexpression and functional dependence [3,8,12,26] |
| MTHFD1L | Mitochondria | Release of formate from 10-formyl-THF | Exportable 1C units, support for cytosolic nucleotide synthesis | Formate overflow and metastatic phenotypes [7,23] |
| MTHFD1 | Cytosol | Re-assimilation and interconversion of folate species | Purine and thymidylate synthesis | Cytosolic compensation for mitochondrial pathway loss [4] |
| MAT2A | Cytosol | SAM synthesis from methionine | Methyl-donor availability, PRMT5 substrate supply | Synthetic lethality in MTAP-deleted cancer [15,21,37] |
| MTAP | Cytosol | MTA salvage | Determines MTA accumulation and PRMT5 vulnerability when deleted | MTAP-loss biology and immune suppression [14,15,36] |

**Table 2. Tumor-intrinsic and immune phenotypes linked to one-carbon metabolism**

| Phenotype | Mechanistic link to 1C metabolism | Key message |
|---|---|---|
| Rapid proliferation | Cytosolic purine and thymidylate synthesis supported by serine-derived 1C units and mitochondrial formate export | 1C flux remains foundational for DNA replication [1,4,24] |
| Hypoxic survival | SHMT2-dependent maintenance of mitochondrial redox balance | 1C metabolism is a stress-adaptation pathway, not only a growth pathway [6] |
| Replication stress tolerance | MTHFD-directed nucleotide support prevents thymidine depletion | MTHFD2/MTHFD1 targeting can expose replication liabilities [18] |
| Metastatic dissemination | Mitochondrial 1C metabolism can preserve motility independent of proliferation | Spatially targeted blockade may suppress metastasis even when cytostasis is limited [23] |
| Tumor PD-L1 expression | MTHFD2 promotes checkpoint-ligand abundance | Metabolic targeting can alter immune evasion directly [12] |
| CD8 T-cell dysfunction | Tumor SLC43A2 depletes methionine and reduces H3K79me2/STAT5 in T cells | Amino acid competition has epigenetic consequences [9] |
| CD4 T-cell exhaustion | Methionine depletion lowers AMPK and raises PD-1 in CD4 T cells | Methionine handling influences helper T-cell checkpoint state [10] |
| Immune resistance in MTAP-loss tumors | MTA accumulation suppresses PRMT5-dependent immune function | MTAP genotype has direct immunologic consequences [14,39] |
| CD8 T-cell rescue | Exogenous formate supports reinvigorated T cells during PD-1 blockade | 1C metabolites can be used to augment immunotherapy [13] |

**Table 3. Therapeutic agents and development status across the one-carbon network**

| Target class | Representative agents | Development stage as of April 21, 2026 | Main translational message |
|---|---|---|---|
| PHGDH | CBR-5884; NCT-503; BI-4916/BI-4924; newer medicinal-chemistry series | Preclinical | Biologically validated, but no peer-reviewed clinical efficacy data yet [16,17,30,31] |
| SHMT1/2 | SHIN2; AGF347 and related folates | Preclinical | Strong proof of concept, especially in leukemia and combination settings [32-34] |
| MTHFD2 / MTHFD1-2 | DS44960156; TH9619; newer selective chemotypes | Preclinical | Mechanistically compelling, including replication-stress and immune-evasion biology, but clinical evidence remains immature [18-20,35] |
| MAT2A | AG-270/S095033; IDE397 | Phase I / I-II | MTAP-guided targeting has clear clinical traction [21] |
| PRMT5 (MTA-cooperative) | AMG 193; MRTX1719; TNG908 | Phase I / I-II | Most clinically advanced 1C-adjacent precision therapy branch in MTAP-deleted tumors [38,39,41-43] |
| Classical antifolates | Methotrexate; pemetrexed; fluoropyrimidines | Approved | Old drugs still define the pathway and remain rational combination partners |

**Table 4. Selected clinically relevant studies targeting the MTAP-MAT2A-PRMT5 axis**

| Agent | Target | Setting | Identifier / source | Current takeaway |
|---|---|---|---|---|
| AG-270/S095033 | MAT2A | Advanced malignancies with MTAP loss enrichment | NCT03435250; published phase I trial [21] | Demonstrated pharmacodynamic target engagement and early clinical activity |
| IDE397 | MAT2A | MTAP-deleted solid tumors | NCT04794699 [42] | Ongoing expansion and combination development |
| AMG 193 | MTA-cooperative PRMT5 | MTAP-deleted solid tumors | NCT05094336; published phase I dose exploration [38] | Objective responses across multiple histologies with manageable safety |
| MRTX1719 | MTA-cooperative PRMT5 | MTAP-deleted solid tumors | NCT05245500 [41] | Clinical development continues with encouraging early activity |
| TNG908 | Selective PRMT5 inhibitor | MTAP-deleted solid tumors | NCT05275478 [43] | Extends clinical testing of MTAP-directed PRMT5 inhibition into additional solid-tumor settings |

## Figure legends

**Figure 1. Compartmentalized one-carbon flux in cancer.** Serine-derived one-carbon units are partitioned across mitochondrial and cytosolic folate metabolism. In mitochondria, SHMT2, MTHFD2, and MTHFD1L convert serine carbon into formate and reducing equivalents, supporting redox control and exporting one-carbon units to the cytosol. In the cytosol, MTHFD1 channels these units into purine and thymidylate synthesis, while the methionine cycle converts methionine into SAM through MAT2A to sustain methylation reactions. Transsulfuration links this network to glutathione production and oxidative-stress buffering. Target nodes emphasized in this review are PHGDH, SHMT1/2, MTHFD2, and MAT2A.

**Figure 2. One-carbon metabolism in the tumor immune microenvironment.** Tumor cells suppress antitumor immunity through several linked one-carbon mechanisms: methionine uptake via SLC43A2 reduces methionine and SAM availability in T cells, MTHFD2 promotes PD-L1 expression, and MTAP loss causes extracellular MTA accumulation that restrains T-cell function. In contrast, extracellular formate can enhance CD8-positive T-cell fitness and improve checkpoint blockade responses in selected preclinical settings. The figure summarizes how tumor-intrinsic and immune-cell one-carbon states converge on exhaustion, checkpoint signaling, and effector competence.

**Figure 3. Therapeutic and biomarker landscape for one-carbon metabolism in cancer.** Therapeutic opportunities can be organized into a precision framework anchored by target class, biological rationale, evidence maturity, and biomarker strategy. PHGDH, SHMT, and MTHFD2 remain largely preclinical and will likely require flux-aware pharmacodynamic readouts. The most mature branch is MTAP-guided targeting of MAT2A or MTA-cooperative PRMT5, where clinical activity has already been reported. Across classes, rational combinations with antifolates, DNA damage response therapy, or immunotherapy are likely to be more effective than pathway monotherapy.

## Conclusions

One-carbon metabolism is often introduced as a housekeeping pathway for proliferating cells, but that description is now too blunt for cancer biology. The more useful view is that 1C metabolism is a **compartmentalized flux architecture** whose outputs are routed toward nucleotide sufficiency, methylation competence, redox control, and immune regulation in context-specific ways. This framework helps unify a diverse literature: why mitochondrial enzymes such as MTHFD2 and SHMT2 are recurrent cancer dependencies, why methionine competition rewires T-cell state, why MTAP deletion creates both tumor-cell vulnerability and immune suppression, and why simple pathway inhibition may fail unless subcellular flux logic is respected.

For translation, three conclusions follow. First, **patient selection must be biology-led**: MTAP deletion is currently the clearest marker, whereas PHGDH amplification and MTHFD2/SHMT2-high states still need better flux-aware stratification. Second, **pharmacodynamics must measure pathway state, not just target occupancy**, because 1C metabolism is defined by moving carbon and methyl units between compartments. Third, **combination therapy is likely to be the rule rather than the exception**, especially with immunotherapy, antifolates, taxanes, and DNA damage response agents. If the field succeeds, the next generation of 1C-directed therapy will not simply “block folate metabolism.” It will reprogram compartmentalized flux to collapse malignant fitness while preserving or restoring immune function.

## List of abbreviations

1C, one-carbon; AHCY, adenosylhomocysteinase; DHFR, dihydrofolate reductase; H3K79me2, histone H3 lysine 79 dimethylation; MAT2A, methionine adenosyltransferase 2A; MTA, methylthioadenosine; MTAP, methylthioadenosine phosphorylase; PD-1, programmed cell death protein 1; PD-L1, programmed death-ligand 1; PHGDH, phosphoglycerate dehydrogenase; PRMT5, protein arginine methyltransferase 5; SAH, S-adenosylhomocysteine; SAM, S-adenosylmethionine; SHMT, serine hydroxymethyltransferase; THF, tetrahydrofolate; TIME, tumor immune microenvironment.

## Declarations

### Ethics approval and consent to participate

Not applicable.

### Consent for publication

Not applicable.

### Availability of data and materials

Data sharing is not applicable to this article because no datasets were generated or analyzed for the present review beyond published literature sources.

### Competing interests

[To be completed by the authors.]

### Funding

[To be completed by the authors.]

### Authors' contributions

[To be completed by the authors.]

### Acknowledgements

[To be completed by the authors.]

### Authors' information

[Optional; to be completed by the authors if desired.]

## References

1. Ducker GS, Rabinowitz JD. One-carbon metabolism in health and disease. Cell Metab. 2017;25(1):27-42.
2. Fan J, Ye J, Kamphorst JJ, Shlomi T, Thompson CB, Rabinowitz JD. Quantitative flux analysis reveals folate-dependent NADPH production. Nature. 2014;510(7504):298-302.
3. Nilsson R, Jain M, Madhusudhan N, Sheppard NG, Strittmatter L, Kampf C, et al. Metabolic enzyme expression highlights a key role for MTHFD2 and the mitochondrial folate pathway in cancer. Nat Commun. 2014;5:3128.
4. Ducker GS, Chen L, Morscher RJ, Ghergurovich JM, Esposito M, Teng X, et al. Reversal of cytosolic one-carbon flux compensates for loss of the mitochondrial folate pathway. Cell Metab. 2016;23(6):1140-53.
5. Possemato R, Marks KM, Shaul YD, Pacold ME, Kim D, Birsoy K, et al. Functional genomics reveal that the serine synthesis pathway is essential in breast cancer. Nature. 2011;476(7360):346-50.
6. Ye J, Fan J, Venneti S, Wan YW, Pawel BR, Zhang J, et al. Serine catabolism regulates mitochondrial redox control during hypoxia. Cancer Discov. 2014;4(12):1406-17.
7. Meiser J, Tumanov S, Maddocks O, Labuschagne CF, Athineos D, Van Den Broek N, et al. Increased formate overflow is a hallmark of oxidative cancer. Nat Commun. 2018;9:1368.
8. Gustafsson Sheppard N, Jarl L, Mahadessian D, Strittmatter L, Schmidt A, Madhusudan N, et al. The folate-coupled enzyme MTHFD2 is a nuclear protein and promotes cell proliferation. Sci Rep. 2015;5:15029.
9. Bian Y, Li W, Kremer DM, Sajjakulnukit P, Li S, Crespo J, et al. Cancer SLC43A2 alters T cell methionine metabolism and histone methylation. Nature. 2020;585(7824):277-82.
10. Pandit M, Sui X, Jin G, Liu Y, Li H, Cai J, et al. Methionine consumption by cancer cells drives a progressive upregulation of PD-1 expression in CD4 T cells. Nat Commun. 2023;14:2930.
11. Li X, Wenes M, Romero P, Huang SC-C, Fendt S-M, Ho P-C. Tumor methionine metabolism drives T-cell exhaustion in hepatocellular carcinoma. Nat Commun. 2021;12:1455.
12. Wang Y-P, Liu J, Liu D, Zhang X, Liu Y, Tan F, et al. The folate cycle enzyme MTHFD2 induces cancer immune evasion through PD-L1 up-regulation. Nat Commun. 2021;12:1940.
13. Rowe JH, Elia I, Shahid O, Gaudiano EF, Sifnugel NE, Johnson S, et al. Formate supplementation enhances antitumor CD8+ T-cell fitness and efficacy of PD-1 blockade. Cancer Discov. 2023;13(12):2706-23.
14. Gjuka D, et al. Enzyme-mediated depletion of methylthioadenosine restores T cell function in MTAP-deficient tumors and reverses immunotherapy resistance. Cancer Cell. 2023;41:1733-1752.e9.
15. Kryukov GV, Wilson FH, Ruth JR, Paulk J, Tsherniak A, Marlow SE, et al. MTAP deletion confers enhanced dependency on the PRMT5 arginine methyltransferase in cancer cells. Science. 2016;351(6278):1214-8.
16. Mullarky E, Lucki NC, Beheshti Zavareh R, Anglin JL, Gomes AP, Nicolay BN, et al. Identification of a small molecule inhibitor of 3-phosphoglycerate dehydrogenase to target serine biosynthesis in cancers. Proc Natl Acad Sci U S A. 2016;113(7):1778-83.
17. Pacold ME, Brimacombe KR, Chan SH, Rohde JM, Lewis CA, Swier LJYM, et al. Intracellular trapping of the selective phosphoglycerate dehydrogenase inhibitor BI-4924 disrupts serine biosynthesis. Nat Chem Biol. 2019;15(5):452-9.
18. Cuthbertson CR, Arabzadeh A, Bankhead A 3rd, Kyani A, Gentry J, Austad SN, et al. Pharmacological targeting of MTHFD2 suppresses acute myeloid leukemia by inducing thymidine depletion and replication stress. Nat Cancer. 2022;3(2):156-72.
19. Kawai J, Toki T, Ota M, Tsuge Y, Motoyama K, Tatsumi C, et al. Structure-based design and synthesis of an isozyme-selective MTHFD2 inhibitor with a tricyclic coumarin scaffold. J Med Chem. 2019;62(22):10204-20.
20. Tedeschi PM, Markert EK, Gounder M, Lin H, Dvorzhinski D, Dolfi SC, et al. Formate overflow drives toxic folate trapping in MTHFD1 inhibited cancer cells. Nat Metab. 2023;5(4):642-59.
21. Rajeshkumar NV, et al. MAT2A inhibitor AG-270/S095033 in patients with advanced malignancies: a phase I trial. Nat Commun. 2025;16:423. doi:10.1038/s41467-024-55316-5.
22. Fan J, Kamphorst JJ, Mathew R, Chung MK, White E, Shlomi T, et al. Glutamine-driven oxidative phosphorylation is a major ATP source in transformed mammalian cells in both normoxia and hypoxia. Mol Syst Biol. 2013;9:712.
23. Kiweler N, Delbrouck C, Pozdeev VI, et al. Mitochondria preserve an autarkic one-carbon cycle to confer growth-independent cancer cell migration and metastasis. Nat Commun. 2022;13:2699. doi:10.1038/s41467-022-30363-y.
24. Maddocks ODK, Labuschagne CF, Adams PD, Vousden KH. Serine metabolism supports the methionine cycle and DNA/RNA methylation through de novo ATP synthesis in cancer cells. Mol Cell. 2016;61(2):210-21.
25. Kim D, Fiske BP, Birsoy K, Freinkman E, Kami K, Possemato RL, et al. SHMT2 drives glioma cell survival in ischaemia but imposes a dependence on glycine clearance. Nature. 2015;520(7547):363-7.
26. Pardo-Lorente N, et al. Nuclear localization of MTHFD2 is required for correct mitosis progression. Nat Commun. 2024;15. doi:10.1038/s41467-024-51847-z.
27. Li AM, Ye J, Leo Wang Y, et al. p53 deficiency induces MTHFD2 transcription to promote cell proliferation and restrain DNA damage. Proc Natl Acad Sci U S A. 2021;118(31):e2100588118.
28. Sugiura A, Andrejeva G, Voss K, Heintzman DR, Xu X, Madden MZ, et al. MTHFD2 is a metabolic checkpoint controlling effector and regulatory T cell fate and function. Immunity. 2022;55(1):65-81.e9.
29. Locasale JW, Grassian AR, Melman T, Lyssiotis CA, Mattaini KR, Bass AJ, et al. Phosphoglycerate dehydrogenase diverts glycolytic flux and contributes to oncogenesis. Nat Genet. 2011;43(9):869-74.
30. Ross KC, Andrews AJ, Marion CD, Yen T-J, Bhattacharjee V. Inhibiting PHGDH with NCT-503 reroutes glucose-derived carbons into the TCA cycle, independently of its on-target effect. Commun Biol. 2021;4:427.
31. Wang Q, Liberti MV, Liu P, et al. Discovery of novel drug-like PHGDH inhibitors to disrupt serine biosynthesis for cancer therapy. J Med Chem. 2023;66(1):747-68.
32. Garcia-Canaveras JC, Lancho O, Ducker GS, Ghergurovich JM, Xu X, da Silva-Diz V, et al. SHMT inhibition is effective and synergizes with methotrexate in T-cell acute lymphoblastic leukemia. Leukemia. 2020;34(12):3097-110.
33. Anderson DD, Woeller CF, Chiang EP, et al. Human SHMT inhibitors reveal defective glycine import as a targetable metabolic vulnerability of diffuse large B-cell lymphoma. Proc Natl Acad Sci U S A. 2018;115(46):E10780-E10789.
34. Wang Y, Schneider C, Chittiboina P, et al. Novel pyrrolo[3,2-d]pyrimidine compounds target mitochondrial and cytosolic one-carbon metabolism with broad-spectrum antitumor efficacy. Mol Cancer Ther. 2019;18(10):1787-801.
35. Chang H-H, Lee L-C, Hsu T, et al. Development of potent and selective inhibitors of methylenetetrahydrofolate dehydrogenase 2 for targeting acute myeloid leukemia: SAR, structural insights, and biological characterization. J Med Chem. 2024;67(23):21106-21125. doi:10.1021/acs.jmedchem.4c01775.
36. Marjon K, Cameron MJ, Quang P, Clasquin MF, Mandley E, Kunii K, et al. MTAP deletions in cancer create vulnerability to targeting of the MAT2A/PRMT5/RIOK1 axis. Cell Rep. 2016;15(3):574-87.
37. Kalev P, Hyer ML, Gross S, Konteatis Z, Chen CC, Fletcher M, et al. MAT2A inhibition blocks the growth of MTAP-deleted cancer cells by reducing PRMT5-dependent mRNA splicing and inducing DNA damage. Cancer Cell. 2021;39(2):209-224.e11.
38. Rodon J, Prenen H, Sacher A, et al. First-in-human study of AMG 193, an MTA-cooperative PRMT5 inhibitor, in patients with MTAP-deleted solid tumors: results from phase I dose exploration. Ann Oncol. 2024;35(12):1138-1147.
39. Chen S, et al. MTA-cooperative PRMT5 inhibitors enhance T cell-mediated antitumor activity in MTAP-loss tumors. J Immunother Cancer. 2024;12(9):e009600.
40. Alhalabi O, et al. MTAP deficiency creates an exploitable target for antifolate therapy in 9p21-loss cancers. Nat Commun. 2022;13:1797. doi:10.1038/s41467-022-29397-z.
41. ClinicalTrials.gov. Phase 1 study of MRTX1719 in solid tumors with MTAP deletion. NCT05245500.
42. ClinicalTrials.gov. Study of IDE397 in participants with solid tumors harboring MTAP deletion. NCT04794699.
43. ClinicalTrials.gov. Study of TNG908 in patients with MTAP-deleted solid tumors. NCT05275478.
