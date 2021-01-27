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

* R2_optimizer

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

