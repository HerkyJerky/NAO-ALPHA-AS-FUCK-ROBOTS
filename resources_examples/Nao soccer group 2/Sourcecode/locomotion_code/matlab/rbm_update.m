function [rbm] = rbm_update(rbm, dW, dbv, dbh)
    rbm.W = rbm.W + dW;
    rbm.bv = rbm.bv + dbv;
    rbm.bh = rbm.bh + dbh;
end
