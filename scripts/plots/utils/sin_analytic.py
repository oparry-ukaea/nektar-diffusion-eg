import numpy as np

#--------------------------------------------------------------------------------------------------
def calc_Chi_n(x,n,L):
    return np.sin(calc_pi_2n_p1(n)*x/2/L)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_lambda_n(n,L):
    return (calc_pi_2n_p1(n)/2/L)**2
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_pi_2n_p1(n):
    return np.pi*(2*n+1)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_AnCnDn_common_denom(n):
    return calc_pi_2n_p1(n)**3
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_An(n, L,Q0,alpha):
    return 16*(L**2)*Q0/calc_AnCnDn_common_denom(n)/alpha
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_Bn(n, T0):
    return 4*T0/calc_pi_2n_p1(n)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_Cn(n, L, Q0):
    return 16*L*calc_CnDn_common_num(n, Q0) / calc_AnCnDn_common_denom(n)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_CnDn_common_num(n, Q0):
    return Q0 * ( ((-1)**n) * calc_pi_2n_p1(n) - 2 ) 
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_Dn(n, L, Q0, alpha, Chi_n):
    return 4*L**2 * calc_CnDn_common_num(n, Q0) / calc_AnCnDn_common_denom(n) / alpha / (Chi_n**2 + 1)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_En(n,L,alpha,Q0,w0,Chi_n):
    return alpha*Q0*calc_pi_2n_p1(n) / 4 / (L*w0)**2 / (Chi_n**2+1)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calcQ(t,Q0,w0):
    return Q0*(1+np.cos(w0*t))/2.
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def calc_Tn(x,t,n,T0,Q0,L,alpha,w0):
    Chi_n = calc_Chi_n(x,n,L)
    lambda_n = calc_lambda_n(n,L)
    exp_term = np.exp(-alpha*lambda_n*t)
    cos_term = np.cos(w0*t)
    sin_term = np.sin(w0*t)

    An = calc_An(n, L,Q0,alpha)
    Bn = calc_Bn(n, T0)
    Cn = calc_Cn(n, L, Q0)
    Dn = calc_Dn(n, L, Q0, alpha, Chi_n)
    En = calc_En(n,L,alpha,Q0,w0,Chi_n)

    result =  An * (1-exp_term) + (Bn - Cn) * exp_term + Dn * (exp_term - cos_term + Chi_n*sin_term) + En * (cos_term + sin_term/Chi_n - exp_term)
    result *= np.sin( calc_pi_2n_p1(n)*x/2/L )
    return result
#--------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------
def calc_analytic(x,t,params,nmax=8):
    # Extract params for clarity
    alpha = params["ALPHA"]
    L     = max(x)
    T0    = params["T0"]
    Q0    = params["Q0"]
    w0    = params["W0"]

    result = T0 + (x**2)*calcQ(t,Q0,w0)/2/L
    for n in range(1,nmax):
        result += calc_Tn(x,t,n,T0,Q0,L,alpha,w0)
    # Apply BC
    result[0] = 0
    return  result
#--------------------------------------------------------------------------------------------------