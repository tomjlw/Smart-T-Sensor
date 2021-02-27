# Customized Cadence Skill Functions

* abBestFit.ils
  * Implemented a linear regression towards wave objects, return the best-fit line and its slope & interception
  * Example usage: abBestFit(fitting_values)
 
* rsq.ils
  * Return the R2(i.e. linearity) score of wave objects 
  * Example usage: rsq(fitting_values)

* rsq_mean.ils
  * Return the mean R2 across specified number of corners, used in optimization only
  * Example usage: rsq_mean(fitting_values number_of_corner) 
