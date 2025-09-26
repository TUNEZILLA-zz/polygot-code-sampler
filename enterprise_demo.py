#!/usr/bin/env python3
"""
Enterprise Demo Generator
Creates business logic comprehensions that showcase real-world use cases
"""

from pcs_step3_ts import PyToIR, render_rust, render_ts, render_go, render_csharp, render_sql

def generate_enterprise_demo():
    """Generate enterprise-focused business logic demos"""
    
    # Business logic examples
    business_examples = [
        {
            "name": "Customer Order Processing",
            "description": "Calculate total revenue from completed high-value orders",
            "python": "sum(order.total * 1.1 for order in orders if order.status == 'completed' and order.total > 100)",
            "use_case": "E-commerce revenue calculation with tax"
        },
        {
            "name": "Employee Performance Analysis", 
            "description": "Find top performers with high sales and low returns",
            "python": "[emp.name for emp in employees if emp.sales > 100000 and emp.return_rate < 0.05]",
            "use_case": "HR analytics and performance reviews"
        },
        {
            "name": "Inventory Management",
            "description": "Identify low-stock items that need reordering",
            "python": "{item.name: item.reorder_level for item in inventory if item.stock < item.reorder_level}",
            "use_case": "Supply chain optimization"
        },
        {
            "name": "Financial Risk Assessment",
            "description": "Calculate portfolio risk for high-risk investments",
            "python": "sum(asset.value * asset.risk_score for asset in portfolio if asset.risk_score > 0.7)",
            "use_case": "Financial services risk management"
        },
        {
            "name": "Customer Segmentation",
            "description": "Identify premium customers for targeted marketing",
            "python": "{customer.id: customer.lifetime_value for customer in customers if customer.lifetime_value > 10000 and customer.engagement_score > 0.8}",
            "use_case": "Marketing automation and personalization"
        }
    ]
    
    print("🏢 **Enterprise Business Logic Showcase**")
    print("=" * 80)
    
    demo_markdown = """
## 🏢 **Enterprise Business Logic Showcase**

*Real-world business logic transformed across all 5 ecosystems:*

"""
    
    for i, example in enumerate(business_examples, 1):
        print(f"\n{i}. {example['name']}")
        print(f"   {example['description']}")
        print(f"   Use Case: {example['use_case']}")
        print(f"   Python: {example['python']}")
        
        # Parse to IR
        parser = PyToIR()
        ir = parser.parse(example['python'])
        
        # Generate sample outputs
        rust_output = render_rust(ir, func_name=f"{example['name'].lower().replace(' ', '_')}_rust")
        csharp_output = render_csharp(ir, func_name=f"{example['name'].replace(' ', '')}CSharp")
        
        demo_markdown += f"""
### {i}. **{example['name']}**

**Business Use Case:** {example['use_case']}

**Python Logic:**
```python
{example['python']}
```

**Rust Implementation:**
```rust
{rust_output}
```

**C# Implementation:**
```csharp
{csharp_output}
```

**Generated SQL:**
```sql
{render_sql(ir, func_name=example['name'].lower().replace(' ', '_'), dialect="postgresql")}
```

---

"""
    
    demo_markdown += """
## 🎯 **Enterprise Benefits**

- **Cross-Team Collaboration**: Python data scientists → Production C#/Rust code
- **Performance Optimization**: Automatic parallel processing across all backends
- **Type Safety**: Compile-time guarantees in Rust, C#, and TypeScript
- **Database Integration**: Direct SQL generation for data processing
- **Maintainability**: Single source of truth in Python, multiple implementations

## 🚀 **Try Enterprise Examples**

```bash
# Customer order processing
python3 pcs_step3_ts.py --code "sum(order.total * 1.1 for order in orders if order.status == 'completed' and order.total > 100)" --target csharp --parallel

# Employee performance analysis  
python3 pcs_step3_ts.py --code "[emp.name for emp in employees if emp.sales > 100000 and emp.return_rate < 0.05]" --target rust --parallel

# Inventory management
python3 pcs_step3_ts.py --code "{item.name: item.reorder_level for item in inventory if item.stock < item.reorder_level}" --target sql --execute-sql
```

**Transform your business logic into production-ready code across all major ecosystems!** ✨
"""
    
    return demo_markdown

if __name__ == "__main__":
    demo = generate_enterprise_demo()
    print(demo)
    
    # Save to file
    with open("ENTERPRISE_SHOWCASE.md", "w") as f:
        f.write(demo)
    
    print("\n💾 Enterprise demo saved to: ENTERPRISE_SHOWCASE.md")
