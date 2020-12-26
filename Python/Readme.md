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

