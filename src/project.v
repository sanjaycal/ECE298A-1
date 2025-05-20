/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_counter_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  reg [7:0] counter_val = 8'd0;

  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin // If reset is active (low)
      counter_val[7:0] <= 8'd0; // Reset counter to 0
    end else begin      // Else, on the rising edge of the clock
      counter_val[7:0] <= counter_val[7:0] + 1; // Increment counter
    end
  end

  //ui_in[0] is the enable input because ena is always on

  assign uo_out[7:0] = 8'd0;
  
  

  assign uio_out = counter_val;
  assign uio_oe  = {8{ui_in[0]}};

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in[7:1], 1'b0};

endmodule
