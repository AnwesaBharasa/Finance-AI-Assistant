from langchain_core.tools import tool

@tool
def calculate_tax_optimization(annual_income: str, deductions: str = "0") -> str:
    """Calculates estimated tax under Old vs New regime in India, and suggests 80C/80D optimizations."""
    annual_income = float(annual_income)
    deductions = float(deductions)
    
    # Old Regime Calculation (Simplified)
    taxable_old = max(0.0, annual_income - deductions)
    tax_old = 0.0
    if taxable_old > 250000.0:
        if taxable_old <= 500000.0:
            tax_old = (taxable_old - 250000.0) * 0.05
            if taxable_old <= 500000.0: tax_old = 0.0 # 87A rebate
        elif taxable_old <= 1000000.0:
            tax_old = 12500.0 + (taxable_old - 500000.0) * 0.20
        else:
            tax_old = 112500.0 + (taxable_old - 1000000.0) * 0.30

    # New Regime Calculation
    taxable_new = annual_income
    tax_new = 0.0
    if taxable_new > 300000.0:
        if taxable_new <= 700000.0:
            tax_new = 0.0 # 87A rebate
        else:
            if taxable_new > 300000.0: tax_new += min(300000.0, taxable_new - 300000.0) * 0.05
            if taxable_new > 600000.0: tax_new += min(300000.0, taxable_new - 600000.0) * 0.10
            if taxable_new > 900000.0: tax_new += min(300000.0, taxable_new - 900000.0) * 0.15
            if taxable_new > 1200000.0: tax_new += min(300000.0, taxable_new - 1200000.0) * 0.20
            if taxable_new > 1500000.0: tax_new += (taxable_new - 1500000.0) * 0.30
            
    best_regime = "Old Regime" if tax_old < tax_new else "New Regime"
    savings = abs(tax_old - tax_new)
    
    return (
        f"Estimated Tax Payable:\n"
        f"- Old Regime (with Rs.{deductions:,.2f} deductions): Rs.{tax_old:,.2f}\n"
        f"- New Regime (no deductions): Rs.{tax_new:,.2f}\n\n"
        f"Recommended: {best_regime} (Saves Rs.{savings:,.2f})\n\n"
        f"Savings Suggestions:\n"
        f"- Section 80C: Invest up to Rs.1.5L in PPF, ELSS, or EPF to significantly lower your Old Regime tax.\n"
        f"- Section 80D: Deduct Health Insurance premiums (up to Rs.25k-Rs.75k) for yourself and your parents."
    )
