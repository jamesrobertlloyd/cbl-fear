function [ t ] = bench_no_graphics( N )
%BENCH_NO_GRAPHICS Summary of this function goes here
%   Detailed explanation goes here
    t1 = clock;
    for n = 1:N
        bench_lu;
        bench_fft;
        bench_ode;
        bench_sparse;
    end
    t2 = clock;
    t = etime(t2, t1);
end

function bench_lu
% LU, n = 1600.
n = 1600;
A = randn(n,n);
tic
lu(A); 
end
% ----------------------------------------------- %
function bench_fft
% FFT, n = 2^21.
n = 2^21;
x = randn(1,n);
tic;
fft(x); 
clear y
fft(x); 
end
% ----------------------------------------------- %
function bench_ode
% ODE. van der Pol equation, mu = 1
F = @vdp1;
y0 = [2; 0]; 
tspan = [0 eps];
[s,y] = ode45(F,tspan,y0);  %#ok Used  to preallocate s and  y   
tspan = [0 400];
n = tspan(end);
tic
[s,y] = ode45(F,tspan,y0); %#ok Results not used -- strictly for timing
end
% ----------------------------------------------- %
function bench_sparse
% Sparse linear equations
n = 300;
A = delsq(numgrid('L',n));
n = size(A, 1);
b = sum(A)';
tic
A\b; %#ok Result not used -- strictly for timing
end

