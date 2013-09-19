function [f] = rbm_free_energy(rbm, x)
f = -x*rbm.bv' + sum(log(1 - rbm_up(rbm, x) + 1e-10), 2);
end
