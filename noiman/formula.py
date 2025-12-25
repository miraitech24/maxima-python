import numpy as np

def get_dTdt(T, e, epsilon, omega, dF_total, alpha):
    Q_orb = (1361*np.cos((13*np.pi)/36)*e**2*np.sin(epsilon)*np.cos(omega)**2)/np.pi+(6805*np.sin((13*np.pi)/36)*e**2*np.cos(epsilon)*np.cos(omega)**2)/36+(2722*np.cos((13*np.pi)/36)*e*np.sin(epsilon)*np.cos(omega))/np.pi+(6805*np.sin((13*np.pi)/36)*e*np.cos(epsilon)*np.cos(omega))/18+(1361*np.cos((13*np.pi)/36)*np.sin(epsilon))/np.pi+(6805*np.sin((13*np.pi)/36)*np.cos(epsilon))/36
    return ((1-alpha)*((1361*np.cos((13*np.pi)/36)*e**2*np.sin(epsilon)*np.cos(omega)**2)/np.pi+(6805*np.sin((13*np.pi)/36)*e**2*np.cos(epsilon)*np.cos(omega)**2)/36+(2722*np.cos((13*np.pi)/36)*e*np.sin(epsilon)*np.cos(omega))/np.pi+(6805*np.sin((13*np.pi)/36)*e*np.cos(epsilon)*np.cos(omega))/18+(1361*np.cos((13*np.pi)/36)*np.sin(epsilon))/np.pi+(6805*np.sin((13*np.pi)/36)*np.cos(epsilon))/36)+dF_total-5.67E-8*(T+288.15)**4)/500
