# Python Scripts for Simulation Data Processing
* R2_optimizer

     A heatmap plot telling the most linear configuration of W/L for differntial ring oscilliator 

  * Usage
    * Simulation
       * Linear sweeping of W, L, T
       * frequency(VT(“/Y3”))

    * Internal Cadence csv file
       * W as row
       * T+L as column: Iterate over all L @ each T
       * frequency as value

    * External Python script
       * Input: csv file path, manually change the range of W,L,T
       * Output: A heatmap plot telling the most linear configuration of W/L 

* VVDDTC2_optimizer

     A script telling the optimized sizing value and lowest 2nd order TC for 2T+Header(Gate connection)  

  * Usage
    * Simulation
       * Linear sweeping of HW, HL, HWW, HLL, T 
       * VVDD of the ideal resistor(/R0/PLUS)

    * Internal Cadence csv file
       * T as row
       * HW/HWW+HL/HLL as column
       * average VVDD as value

    * External Python script
       * Input: csv file path 
       * Output: optimized 2nd TC value & corresponding sizing configuration  

* VVDD_Construct

     A script combing rofreq value from different assigned VVDD for different corners
  
  * Usage
    * Simulation
       * Linear sweeping of VVDD

     * Internal Cadence csv file
       * T as row with first line as header indicating corner
       * Using leafvalue function to extract frequency one by one VVDD
       * Put in an Excel, just a chunk of data with dimension (N_VVDD, N_TK, N_Corner) no spacing needed 
     
     * External Python script
       * Input: csv file path, some constatnt determining spacing of VVDD, VVDD @ TT and N_TK
       * Output: Overall sigma value     

* res_readout

     A script displaying dashboard of relationship between design parameters for readout and resolution
  
  * Usage
    * Simulation
       * Linear sweeping of VVDD

     * Internal Cadence csv file
       * T as row with first line as header indicating corner
       * Put in an Excel, just a chunk of data with dimension (N_VVDD, N_TK, N_Corner) no spacing needed 
     
     * External Python script
       * Input: csv file path
       * Output: Dashboard help determine #total and #sample

* error_plot

     A script calculating the 3-sigma as temperature sensor's accuracy
  
  * Usage
    * Simulation
       * Linear sweeping of VVDD

     * Internal Cadence csv file
       * T as row with first line as header indicating corner
       * Put in an Excel, just a chunk of data with dimension (N_VVDD, N_TK, N_Corner) no spacing needed 
     
     * External Python script
       * Input: csv file path
       * Output: 3sigma value
       
* FOM_plot

     A script generates a FOM graph used in paper
  
  * Usage
    * Source file
       * Download Makinwwa's famous Tsensor survey
     
     * External Python script
       * Input: survey file path, user-defined fiter condition & graph details
       * Output: FOM graph

