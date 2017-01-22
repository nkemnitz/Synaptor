#!/usr/bin/env julia

#parameters.jl
#-------------------------------
# relatively stable parameters for input data

#A name for each volume in the network output
vol_map = Dict(
  "boundary" => 1,
  "axon"     => 2,
  "dendrite" => 3,
  "non-PSD"  => 4,
  "PSD"      => 5
)

#Connected components threshold
cc_thresh = 0.35
#Size threshold
size_thresh = 200
#Dilation distance parameter
dilation_param = 15

#Datatypes of inputs&outputs
sem_dtype = Float32
seg_dtype = UInt32

#Polygon mask filename
# Useful if your data doesn't fill the whole volume
# or significant output artifacts exist
mask_poly_fname = nothing;

#=================================
#out-of-core parameters
=================================#
scan_chunk_shape = [1024,1024,128];

DEBUG=false;
