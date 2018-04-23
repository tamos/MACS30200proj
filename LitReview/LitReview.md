## The Push-Pull Paradigm

One way migration is often studied is as the result of push and pull factors. Push factors drive individuals to leave locations, while pull factors attract them to others. [@edwardschaos] Within forced migration studies, there is an abundance of qualitative and normative literature exploring these factors. However, compared to studies of commuting and econometric models of trade there are relatively few empirical, formal, and simulation-based studies of forced migration. Moreover, this area of research is currently of little use to practitioners, who require more granular results in order to make decisions. 

## Structure of the Review

This review proceeds in three parts. First, it outlines two leading models from migration studies and economics. Second, it explores the viability of simulation in general, as well as two specific types of simulation, in modelling and forecasting features of displacement events. Third, it concludes with an outline for how future research may judged in terms of its usefulness to practitioners. 

### The Gravity Model

The most prominent of formal migration models is the gravity model. First used to explain economic migration [See @ravenstein1885; in @edwardschaos], it is frequently employed in econometric studies of trade, with some applications to forced migration. [@iqbal2007geo; in @edwardschaos] In this analogy to the phenomena in physics, individuals are "objects" which are drawn to one or other locations by the "mass" of the location. The attractive power (mass) of a location is determined by some characteristic, usually population. [@edwardschaos] This attraction is then limited by a function (usually distance) which is assumed to have a negative relationship with attraction; closer locations are preferred to those more distant. 

(@gravity) $$ I_{i,j} = \frac{f(R_i, A_j)}{f(D_{i,j})} $$
Where $I$ is the interaction between locations $i$ and $j$, determined by $R_i$, repelling forces at location $i$ and $A_j$, attraction at location $j$. $D_{i,j}$ is the distance between locations $i$ and $j$. [@edwardschaos pp 21] ^[See @simini2012universal for a concise description of both the gravity and radiation models.]

For its robustness across a number of applications, long history, and appealing simplicity, the gravity model overemphasizes macro trends. [@edwardschaos pp 21] Simini et al. [-@simini2012universal] identify a number of further issues: i) the wide latitude available in determining the cost function $f(D_{i,j})$; ii)  poor predictive performance in certain applications; iii) an over-reliance on population, and; iv) a number of free parameters. These, and other points, are addressed by an alternative which draws from another physics metaphor - the radiation model. ^[Other alternatives exist, such as the intervening opportunity or random utility models. [@simini2012universal]]

### The Radiation Model

In the radiation model proposed by Simini et al. [-@simini2012universal], an individual considers movement to all areas, including their current area of residence. The individual evaluates the relative attractiveness of all areas on the basis of some "offer". In the original formulation, this is an employment offer. The individual then chooses the closest offer which is at least some threshold higher than the most attractive offer in their current location. [@simini2012universal]

(@radiation) $$ T_{ij} = T_i \frac{m_i n_j}{(m_i + s_{ij}) (m_i + n_j + s_{ij})} $$
Where locations $i$ and $j$ have populations of size $m$ and $n$. The distance between locations is represented by $r_{ij}$ and $s_{ij}$ is the total population in a circle with a radius $r_{ij}$. The centre of this circle is $i$, and the population $s_{ij}$ excludes $m + n$. $T_{ij}$ represents the total "flux" or commuting volume from location $i$ to location $j$. 

In analyses comparing the radiation and gravity models using city-level commuting data, the radiation and gravity models offer similar results, but the radiation model has the additional advantage of being simpler and does not have free parameters. [@masuccigravityvsradiation; @simini2012universal] As a new proposal, it remains an active area of migration modelling research.^[See, for example, the updated model in @siminiradiation2013] 

### Persistent Rationality Assumption

Both gravity and radiation models are drawn from economic and demographic studies of commuting and more routine forms of migration. This leads them to rely on certain assumptions commonly found in rational choice models. [@edwardschaos pp 20-22] These models assume an individual chooses to move from one location to another on the basis of some rational calculus - weighing the benefits and costs of staying or leaving. [@edwardschaos pp 16] 

The rationality assumption can be a useful approximation of human decision-making in many environments. Both the radiation and gravity model perform well despite this assumption. In forced migration studies, however, the objects of analysis are regularly coerced and operate in environments with poor information flow. As such, the rationality assumption may be a substantial theoretical weakness. (Ibid)

### Robustness to Reality and Relaxing the Rationality Assumption

In search of greater robustness, some mixed models use elements of the above models with new approaches from areas such as network theory. An informal variant bears some similarities to the gravity model. In this model, the attractiveness of a location is determined by presence of more migrant individuals at a given location. As more migrant individuals arrive, that location gains more attractiveness because of the social ties between the origin and destination. [@lindstrompioneer; @GaripAsad] More formal alternatives combine heuristics based on formal models from the push-pull paradigm with network or graph models. [@ahmed2016multi; @suleimenova2017generalized] Edwards [-@edwardschaos] explores ways to account for a relaxed rationality assumption in detail, presenting an agent-based model on a generic lattice which combines elements of macro models (e.g., gravity) and observations from research at the micro level like the limitations of the rational choice assumption (e.g., informational assymmetry). Most recently, Suleimanova et al. [-@suleimenova2017generalized] do not relax the rationality assumption of the agent, but instead develop a network based on a network of real-world locations and events which agents traverse in a simulation according to a set of rules inspired in part by the gravity model (@gravity). 

## Value of Simulation in Forced Migration Studies

Simulation studies have potential for a number of interesting applications in forced migration studies. The principal benefits are fourfold: i) experimental imitation, [@hartmann1996 pp 2-10; in @edwardschaos]; ii) the ability to explore the internal dynamics of a phenomenon when the management, modelling or collection of detailed data is not feasible (Ibid); iii) apart from time, little to no cost for the researcher, and; iv) no need for specialized knowledge beyond intermediate programming. The first is necessary because experiments to generate displacement are neither ethical nor practical. The second is useful because data on displacement can be missing or unreliable - data collection is not a first priority for actors on the ground. The third and fourth make simulation useful for non-profits and resource-poor organizations. These last two points also give simulation a clear advantage for researchers hoping for wider adoption of their techniques by practitioners. 

Simulation overcomes the challenges outlined above with certain costs. Most germane to this discussion are those of generalizability and realism. ^[See @maldonadosimulationcritical pp 454-455 for a more extensive discussion.] Simulations are questionably generalizable, as they are only valid under the specific scenarios (i.e., combinations of parameters and assumptions) used by the researchers. Furthermore, simulations are only approximations of reality, capturing but a fraction of the true complexity in social phenomena. In a purely theoretical study, this second objection is of less concern, but when a more applied orientation is adopted, this shortcoming raises substantial questions about the "real world" implications of simulation studies. Maldonado and Greenland [-@maldonadosimulationcritical] propose  the results from simulations should be interpreted similar to clinical studies in medicine, with: i) great caution; ii) requirement for corroboration, and; iii) reference to real-world data. 

Researchers using simulation in forced migration studies account for these challenges by employing complex, multi-layered models [@edwardschaos], or basing their simulations on real parameters (e.g., locations and distances between those locations) of a specific instance of the phenomena of interest. [@suleimenova2017generalized] The challenge of demonstrating real-world validity can also be addressed by structuring a simulation to produce predictions which can then be compared to real-world data.^[One example of this strategy is found in @suleimenova2017generalized.]

## Implementing Simulations

Reasonable approximations of displacement via simulation are achieved through a number of methods. While many methods exist, this review borrows from comparative politics and adopts the "most different" approach. First, it discusses the features of random walks, which relies the least on assumptions. Second, agent-based models, which require many assumptions.

### Random Walks

The movement of displaced people can be thought of as a random walk, where displaced people move between points according to some set of probabilities defined by a specified function. ^[One well-known example is Lévy flight.] This approach is used to model the movement of animal populations in biology and everyday human movement. [@codlingrandomwalks; @bovet1988spatial; @gallotti2016stochastic] It may have some application in the study of forced migration - a random walk simulation from the International Organziation for Migration reportedly predicts displacement trends with error rates less than 10%. [@iomrandomwalk] ^[This claim is yet to be tested in a peer-reviewed publication.]

For their apparent robustness, random walks have questionable theoretical value for research in forced migration. If a process of forced migration is in fact a random walk, how does one interpret the results of a given simulation? What do simulation results say about the experience of displaced people? To the author's knowledge, there is no systematic way to interpret random walks to answer such questions. Nevertheless, random walks' ability to "blindly" model real phenomena makes them useful as a benchmark against which to compare more sophisticated models - a "uniform probability plus" of sorts. If a random walk outperforms more theoretically-informed models, this should be interpreted as weakness in the sophisticated model, rather than support of any "chaos" theory of forced migration. 

### Agent-based Models

Agent-based simulations require the modeller to specify all rules by which individuals make decisions. This makes explicit the connection between results and theory. In a displacement simulation, agents (a household or individual) move across a virtual space and interact with elements of the simulation according to some set of rules. ^[See @edwardschaos for an accessible explanation of agent-based models.] Beyond its proven ability to model a wide range of phenomena, this approach is intuitively understood by non-technical audiences and is relatively simple to implement. 

Many of the critiques of simulation generally, such as those from Maldonado and Greenland [-@maldonadosimulationcritical] apply to agent-based models in particular. The rules by which agents "live" may be unreasonable simplifications or require bold assumptions which, in the worst case, limit simulation results' generalizability to just other simulations. This is notable given one of the reasons for choosing simulation methods is to manipulate virtual ecosystems to enhance understanding of real ones.

### Macro Models, Micro Requirements

Clearly formal models borrowed from economics (gravity, radiation), and simulation methods (random walks, agent-based models) have potential to produce valuable insights in forced migration studies. Yet there remain a number of gaps in this literature. Specifically, forced migration simulations mostly provide macro-level results with questionable generalizability. micro-level results with high generalizability would most benefit efforts to respond to crisis and conflict. Moving forward, what characteristics should models have in order to be relevant in this way?

  i) _Micro focus:_ Models must unpack phenomena with greater granularity. While intra-regional analyses of migration flows, such as Iqbal [-@iqbal2007geo] may provide useful insights for long-term planning, they do not contribute to preparedness or response within a given country.
      
  ii) _Focus on actionable insights:_ A substantial amount of empirical work in this space focuses on  causal drivers of displacement. Researchers investigate how significant events, regimes, or geographical scope and intensity of conflict effect movement patterns. [@schonj; @melanderoberg] These studies produce insightful results about broad displacement trends. However for practical purposes like humanitarian response, more specific results about volume and geographic distribution of displaced people in-country are valuable. 
      
  iii) _Employ integrated models of displacement and return:_ To the author's knowledge, no empirical studies have examined displacement and return as integrated phenomena. Displacement is only part of the displaced individual's experience, and displaced people can and do return to their communities of origin. Needs persist from displacement through to return and so the ability to model the lifecyle of a displacement event is valuable. 
      
  iv) _Be robust to the displaced populations' legal status:_  The experiences of refugees and internally displaced people have many commonalities. The distinction is primarily legal. ^[For this reason, this review has not distinguished between these two populations. See Loescher et al. [-@loescher2008united] for more nuance on this issue.] Models should therefore be robust across both internally displaced and refugee populations. 

Research which can address one or more of these points will fill important extant gaps in the literature on forced migration simulation. Moreover, it will address an important ethical imperative - research which focuses on negative human experiences must in some way contribute to alleviating or preventing that experience. ^[This point was first made to the author in 2013 by James Milner during an undergraduate seminar at Carleton University.]
\newpage

# References

---
title: "Computational Models For Simulating Forced Migration: An Overview of Leading Methods"
author: Tyler Amos
date: 23 April 2018
abstract: "This methodological review examines current and emergent research in simulating forced migration, with an eye to real-world applications. It examines gravity and radiation models, random walks and agent-based implementations, and provides suggestions for future research to be relevant for humanitarian practice."

bibliography: Simulating-Displacement-LitReview.bib
    
---

[compile and install instructions]: <> ( To compile run in shell: pandoc inputfilename -o outputfilename --filter pandoc-citeproc
To install pandoc-citeproc: brew install pandoc pandoc-citeproc 
To install latex: brew install caskroom/cask/basictex 
Ref: https://stackoverflow.com/questions/4823468/comments-in-markdown#20885980
Ref: http://www.chriskrycho.com/2015/academic-markdown-and-citations.html
Ref: https://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)