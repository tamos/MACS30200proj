---
output:
  html_document: default
  pdf_document: default
---
# Problem Set 1

### MACSS 30200

_Tyler Amos_

16-Apr-2018

## Data Description

Access: This dataset can be downloaded from the Centers for Disease Control and Prevention (CDC) website (www.cdc.gov) as a compressed (e.g., .zip, .dat.Z) file. A derivation of this dataset is also available from the National Bureau of Economic Research website (www.nber.org) in a variety of formats (e.g., Stata, SAS).

Curation: The data is curated in its original source by the CDC through the National Center for Health Statistics' National Vital Statistics System. The National Bureau of Economic Research curates the derived datasets. 

Previous studies have used this data to study...


2. Cite other key papers that have used this data.

Shih, Tiffany, Desi Peneva, Xiao Xu, Amelia Sutton, Elizabeth Triche, Richard A. Ehrenkranz, Michael Paidas, and Warren Stevens. "The rising burden of preeclampsia in the United States impacts both maternal and child health." American journal of perinatology 33, no. 04 (2016): 329-338.

Shahabi, Ahva, Desi Peneva, Devin Incerti, Kimmie McLaurin, and Warren Stevens. "Assessing variation in the cost of palivizumab for respiratory syncytial virus prevention in preterm infants." PharmacoEconomics-open 2, no. 1 (2018): 53-61.

DeLeire, Thomas, Leonard M. Lopoo, and Kosali I. Simon. "Medicaid expansions and fertility in the United States." Demography 48, no. 2 (2011): 725-747.

Walton, Emily. "Residential segregation and birth weight among racial and ethnic minorities in the United States." Journal of health and social behavior 50, no. 4 (2009): 427-442.

Lopoo, Leonard M., and Thomas DeLeire. "Did welfare reform influence the fertility of young teens?." Journal of Policy Analysis and Management 25, no. 2 (2006): 275-298.

Henshaw, Stanley K., and Dina J. Feivelson. "Teenage abortion and pregnancy statistics by state, 1996." Family Planning Perspectives (2000): 272-280.


3. Describe how the data were collected.

The data were consolidated from a 100% sample taken from birth records in US states. 


### Descriptive Statistics

_Outliers and missing data have been removed._

#### Numeric Variables

| Code  | Description  | Max | Min | Std | Mean | 
|---|---|---|---|---| --- |
|`dob_tt`   | Time of Birth in minutes elapsed that day | 2400 |  0  |  640 | 1231 |  
| `mager`   | Mother's age in years | 50|  12  |  5.8 | 28.7 |  
| `fagecomb`   | Father's age in years | 98 |  11  |  22.7 | 39.5 |  
| `priorlive`   | Number of children by the same mother who are still living | 21 |  0  |  4.6 | 1.3 |

#### Categorical Variables

| Code  | Description  | Mode | Visualization | 
|---|---|---|---|
| `dob_mm`   | Month of Birth | August |  Distribution of Births by Month  |
| `dob_wk`   | Day of the Week of Birth | Tuesday |  Distribution of Births by Day of the Week  |
| `meduc`   | Mother's Educational Attainment | High School Graduate/GED |  Mother's Educational Attainment  |
| `feduc`   | Father's Educational Attainment | High School Graduate/GED |  Father's Educational Attainment  |

One trend which is most apparent from exploratory analysis is the role sex plays in determining the timing of children relative to educational attainment. 

![Note that while higher levels of education appears to delay fatherhood, this is not strictly true in the upper age ranges. ](Fathersageandeducation.png)


![Here we can see clearly that while mothers' data displays the same trend with respect to educational attainment as fathers', the ceiling on women's fertility around the age of 50 is apparent. ](Mothersageandeducation.png)

####  Disaggregation by Education Across Selected Variables

6. Show at least one conditional (slice) description of the data (e.g., all variable descriptive statistics by nationality of survey respondent). This can be a table or visualization.

#### Sliced Data by Mother's Educational Attainment

![Number of Living Children and Mother's Education ](Priorliveandeducation.png)

![Mother's Age and Education ](Mothersageandeducation.png)


![Mother and Father's Education ](FatherandMothereducation.png)

![Birth Time and Mother's Education ](Birthtimeandeducation.png)

![Birth Day and Mother's Education ](Birthdayandeducation.png)

![Birth Month and Mother's Education ](Birthmonthandeducation.png)


![Father's Age and Mother's Education ](Fathersageandmotherseducation.png)




## Research Paper Critique

Paper: http://journals.sagepub.com/doi/pdf/10.1177/1440783313495765

1. State the research question of your assigned paper.

2. What data did the paper use?

3. What theory did the paper reference in order to interpret the data? (Note: it is possible that the paper has no reference to theory.)

4. Was your assigned paper a descriptive study, an identification exercise, a numerical solution to system of equations study, or some combination of the three? (These are the three classifications we discussed in class.)

5. What computational methods did this paper use to answer the research question? What was their result or answer to the question?

6. Think of yourself as an academic referee. Give two suggestions to the author(s) of your assigned paper of things the authors might do to improve their results or strengthen their evidence for the answer to the question.
