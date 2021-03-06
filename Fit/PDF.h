#pragma once

#include <vector>

#include <RooAbsPdf.h>
#include <RooRealVar.h>
#include <RooExponential.h>
#include <RooChebychev.h>
#include <RooListProxy.h>

#include <Math/PdfFuncMathCore.h>

class LaurentPdf : public RooAbsPdf {
  public:
    LaurentPdf() {} ; 
    LaurentPdf(const char *name, const char *title, int _firstPow, int _lastPow, RooAbsReal& _x, const RooArgList& _coefList):
      RooAbsPdf(name, title),
      firstPow(_firstPow), lastPow(_lastPow),
      x("x", "x", this, _x),
      coefList("coefficients", "list of coefficients", this) {

        if (_coefList.getSize() != abs(firstPow - lastPow)) {
          std::cout << "Error: arguments list must have " << abs(firstPow - lastPow) << " parameters." << std::endl;
          assert(0);
        }

        TIterator* coefIter = _coefList.createIterator();
        RooAbsArg* coef;
        while((coef = (RooAbsArg*)coefIter->Next())) {
          if (!dynamic_cast<RooAbsReal*>(coef)) {
            std::cout << "Laurent::ctor(" << GetName() << ") ERROR: coefficient " << coef->GetName() 
              << " is not of type RooAbsReal" << std::endl;
            assert(0);
          }
          coefList.add(*coef);
        }
        delete coefIter;
      };

    LaurentPdf(const LaurentPdf& other, const char* name = NULL):
      RooAbsPdf(other, name),
      firstPow(other.firstPow), lastPow(other.lastPow),
      x("x", this, other.x),
      coefList("coefList", this, other.coefList) {};

    virtual TObject* clone(const char* newname) const { return new LaurentPdf(*this, newname); }
    inline virtual ~LaurentPdf() { }

  protected:

    int firstPow;
    int lastPow;
    RooRealProxy x;
    RooListProxy coefList;

    double evaluate() const {
      double sum = 0.;
      int index = 0;
      for (int p = firstPow; p >= lastPow; p--, index++) {
        if (p == lastPow) {
          double coefSum = 0;
          for (int i = 0; i < coefList.getSize(); i++) {
            coefSum += ((RooAbsReal&) coefList[i]).getVal();
          }
          sum += (1 - coefSum) * 1e4 * pow(x / 1e-6, p);
        } else {
          sum += ((RooAbsReal&) coefList[index]).getVal() * 1e4 * pow(x * 1e-6, p);
        }
      }

      return sum;
    };
};

class FAltPdf : public RooAbsPdf {
  public:
    FAltPdf() {} ; 
    FAltPdf(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _a, RooAbsReal& _b, RooAbsReal& _c):
      RooAbsPdf(name, title),
      x("x", "x", this, _x),
      a("a", "a", this, _a),
      b("b", "b", this, _b),
      c("c", "c", this, _c) {};

    FAltPdf(const FAltPdf& other, const char* name = NULL):
      RooAbsPdf(other, name),
      x("x", this, other.x),
      a("a", this, other.a),
      b("b", this, other.b),
      c("c", this, other.c) {};

    virtual TObject* clone(const char* newname) const { return new FAltPdf(*this, newname); }
    inline virtual ~FAltPdf() { }

  protected:

    RooRealProxy x;
    RooRealProxy a;
    RooRealProxy b;
    RooRealProxy c;

    double evaluate() const {
      return pow((1. - (x / 8000.)), a) / pow((x / 8000.), (b + c * log(x / 8000.)));
    };
};

class FAltBPdf : public RooAbsPdf {
  public:
    FAltBPdf() {} ; 
    FAltBPdf(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _a, RooAbsReal& _b, RooAbsReal& _c):
      RooAbsPdf(name, title),
      x("x", "x", this, _x),
      a("a", "a", this, _a),
      b("b", "b", this, _b),
      c("c", "c", this, _c) {};

    FAltBPdf(const FAltBPdf& other, const char* name = NULL):
      RooAbsPdf(other, name),
      x("x", this, other.x),
      a("a", this, other.a),
      b("b", this, other.b),
      c("c", this, other.c) {};

    virtual TObject* clone(const char* newname) const { return new FAltBPdf(*this, newname); }
    inline virtual ~FAltBPdf() { }

  protected:

    RooRealProxy x;
    RooRealProxy a;
    RooRealProxy b;
    RooRealProxy c;

    double evaluate() const {
      double xover = x / 8000.;
      double up = pow(((1. - xover + c * pow(xover, 2.))), a);
      double down = pow(x, b);

      if (std::isinf(down)) {
        return 0.;
      } else if (std::isinf(up)) {
        return std::numeric_limits<double>::max();
      }

      return up / down;
    };
};

class FAltCPdf : public RooAbsPdf {
  public:
    FAltCPdf() {} ; 
    FAltCPdf(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _a, RooAbsReal& _b):
      RooAbsPdf(name, title),
      x("x", "x", this, _x),
      a("a", "a", this, _a),
      b("b", "b", this, _b) {};

    FAltCPdf(const FAltCPdf& other, const char* name = NULL):
      RooAbsPdf(other, name),
      x("x", this, other.x),
      a("a", this, other.a),
      b("b", this, other.b) {};

    virtual TObject* clone(const char* newname) const { return new FAltCPdf(*this, newname); }
    inline virtual ~FAltCPdf() { }

  protected:

    RooRealProxy x;
    RooRealProxy a;
    RooRealProxy b;

    double evaluate() const {
      return pow(1. - (x / 8000), a) / pow(x, b);
    };
};

class UFOPdf : public RooAbsPdf {
  public:
    UFOPdf() {} ; 
    UFOPdf(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _a, RooAbsReal& _b):
      RooAbsPdf(name, title),
      x("x", "x", this, _x),
      a("a", "a", this, _a),
      b("b", "b", this, _b) {};

    UFOPdf(const UFOPdf& other, const char* name = NULL):
      RooAbsPdf(other, name),
      x("x", this, other.x),
      a("a", this, other.a),
      b("b", this, other.b) {};

    virtual TObject* clone(const char* newname) const { return new UFOPdf(*this, newname); }
    inline virtual ~UFOPdf() { }

  protected:

    RooRealProxy x;
    RooRealProxy a;
    RooRealProxy b;

    double evaluate() const {
      /*std::cout << "x: " << x << std::endl;
      std::cout << "a:" << a << std::endl;
      std::cout << "b: " << b << std::endl;*/
      double val = 1. / (1. + exp(((x / 8000) - a) / b));
      /*std::cout << val << std::endl;*/

      return val;
    };
};

class PowPdf : public RooAbsPdf {
  public:
    PowPdf() {} ; 
    PowPdf(const char *name, const char *title, RooAbsReal& _x, RooAbsReal& _a):
      RooAbsPdf(name, title),
      x("x", "x", this, _x),
      a("a", "a", this, _a) {};

    PowPdf(const PowPdf& other, const char* name = NULL):
      RooAbsPdf(other, name),
      x("x", this, other.x),
      a("a", this, other.a) {};

    virtual TObject* clone(const char* newname) const { return new PowPdf(*this, newname); }
    inline virtual ~PowPdf() { }

  protected:

    RooRealProxy x;
    RooRealProxy a;

    double evaluate() const {
      return pow(x, -1. * a);
    };
};

class GammaPlusLogNormalPdf : public RooAbsPdf {
  public:
    GammaPlusLogNormalPdf() {};
    GammaPlusLogNormalPdf(const char *name, const char *title, RooAbsReal& _x,
                                                // Gamma PDF
                                                RooAbsReal& _alpha, RooAbsReal& _theta,
                                                // Log normal PDF
                                                /*RooAbsReal& _mu,*/ RooAbsReal& _sigma,
                                                // Various
                                                RooAbsReal& _shift, RooAbsReal& _sum):
      RooAbsPdf(name, title),
      x("x", "x", this, _x),
      alpha("alpha", "alpha", this, _alpha),
      theta("theta", "theta", this, _theta),
      //mu("mu", "mu", this, _mu),
      sigma("sigma", "sigma", this, _sigma),
      shift("shift", "shift", this, _shift),
      sum("sum", "sum", this, _sum) {};

    GammaPlusLogNormalPdf(const GammaPlusLogNormalPdf& other, const char* name = NULL):
      RooAbsPdf(other, name),
      x("x", this, other.x),
      alpha("alpha", this, other.alpha),
      theta("theta", this, other.theta),
      //mu("mu", this, other.mu),
      sigma("sigma", this, other.sigma),
      shift("shift", this, other.shift),
      sum("sum", this, other.sum) {};

    virtual TObject* clone(const char* newname) const { return new GammaPlusLogNormalPdf(*this, newname); }
    inline virtual ~GammaPlusLogNormalPdf() { }

  protected:

    RooRealProxy x;

    // Gamma PDF
    RooRealProxy alpha; // On Wikipedia, it's 'k'
    RooRealProxy theta;

    // Log normal PDF
    //RooRealProxy mu;
    RooRealProxy sigma;

    RooRealProxy shift;
    RooRealProxy sum;

    double evaluate() const {

      // Constrain 'mu' with other parameters

      // Mode of lognormal distribution: M_log = exp(mu - sigma^2)
      // Mode of gamma distribution: M_gamma = (alpha - 1) * theta
      // Impose M_log == M_gamma

      double constrained_mu = std::log((alpha - 1) * theta) + sigma * sigma;

      double lognormal = ROOT::Math::lognormal_pdf(x, constrained_mu, sigma, shift);
      double gamma = ROOT::Math::gamma_pdf(x, alpha, theta, shift);

      return sum * lognormal + (1. - sum) * gamma;
    };
};

class GammaPdf : public RooAbsPdf {
  public:
    GammaPdf() {};
    GammaPdf(const char *name, const char *title, RooAbsReal& _x,
                                                // Gamma PDF
                                                RooAbsReal& _alpha, RooAbsReal& _theta,
                                                // Various
                                                RooAbsReal& _shift):
      RooAbsPdf(name, title),
      x("x", "x", this, _x),
      alpha("alpha", "alpha", this, _alpha),
      theta("theta", "theta", this, _theta),
      shift("shift", "shift", this, _shift) {};

    GammaPdf(const GammaPdf& other, const char* name = NULL):
      RooAbsPdf(other, name),
      x("x", this, other.x),
      alpha("alpha", this, other.alpha),
      theta("theta", this, other.theta),
      shift("shift", this, other.shift) {};

    virtual TObject* clone(const char* newname) const { return new GammaPdf(*this, newname); }
    inline virtual ~GammaPdf() { }

  protected:

    RooRealProxy x;

    // Gamma PDF
    RooRealProxy alpha; // On Wikipedia, it's 'k'
    RooRealProxy theta;

    RooRealProxy shift;

    double evaluate() const {


      // Mode of gamma distribution: M_gamma = (alpha - 1) * theta

      double gamma = ROOT::Math::gamma_pdf(x, alpha, theta, shift);

      return gamma;
    };
};

