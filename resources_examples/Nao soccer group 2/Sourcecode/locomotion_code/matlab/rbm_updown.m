function [v, pv, h, ph] = rbm_updown(rbm, v)
    ph = rbm_up(rbm, v);
    h = rbm_sample(ph);
    pv = rbm_down(rbm, h);
    v = pv;
end
