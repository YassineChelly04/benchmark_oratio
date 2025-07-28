"""
Legal Tech Competitor Research System - Master Orchestrator
Coordinates all three parts using MCP server architecture
"""

import os
import sys
import time
from datetime import datetime

# Import the three parts
from part1_company_discovery import run_part_1
from part2_company_research import run_part_2
from part3_excel_export import run_part_3

class LegalTechResearchOrchestrator:
    def __init__(self, groq_api_key="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"):
        self.groq_api_key = groq_api_key
        self.start_time = datetime.now()
        self.results = {
            'part1_companies': 0,
            'part2_researched': 0,
            'part3_excel_created': False,
            'total_time': 0
        }

    def run_complete_research(self):
        """Run the complete 3-part research system"""
        print(">> Legal Tech Competitor Research System")
        print("=" * 60)
        print("TARGET: Oratio Technologies Competitor Analysis")
        print("AI MODEL: DeepSeek-R1-Distill-Llama-70B via Groq")
        print("ARCHITECTURE: MCP Multi-Agent System")
        print("=" * 60)
        
        try:
            # Part 1: Company Discovery
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting Part 1...")
            companies = self.run_part_1_with_monitoring()
            
            if not companies:
                print("ERROR: Part 1 failed - no companies discovered")
                return False
            
            # Part 2: Detailed Research  
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting Part 2...")
            research_results = self.run_part_2_with_monitoring()
            
            if not research_results:
                print("ERROR: Part 2 failed - no research data generated")
                return False
            
            # Part 3: Excel Export
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Starting Part 3...")
            excel_success = self.run_part_3_with_monitoring()
            
            if not excel_success:
                print("ERROR: Part 3 failed - Excel file not created")
                return False
            
            # Complete success
            self.calculate_final_results()
            self.print_final_summary()
            return True
            
        except Exception as e:
            print(f"CRITICAL ERROR in research orchestrator: {e}")
            return False

    def run_part_1_with_monitoring(self):
        """Run Part 1 with progress monitoring"""
        try:
            print("PART 1: Company Discovery Agent")
            print("-" * 40)
            
            # Run company discovery
            companies = run_part_1()
            
            if companies:
                self.results['part1_companies'] = len(companies)
                print(f"SUCCESS: Part 1 Complete - {len(companies)} companies discovered")
                
                # Show breakdown
                direct = len([c for c in companies if c.get('relevance') == 'direct'])
                indirect = len([c for c in companies if c.get('relevance') == 'indirect']) 
                peripheral = len([c for c in companies if c.get('relevance') == 'peripheral'])
                
                print(f"   - Direct competitors: {direct}")
                print(f"   - Indirect competitors: {indirect}")
                print(f"   - Peripheral companies: {peripheral}")
                
                return companies
            else:
                print("ERROR: Part 1 failed to discover companies")
                return None
                
        except Exception as e:
            print(f"ERROR: Part 1 - {e}")
            return None

    def run_part_2_with_monitoring(self):
        """Run Part 2 with progress monitoring"""
        try:
            print("\nPART 2: Multi-Agent Company Research")
            print("-" * 40)
            print("AGENTS: Web Search, Website Analysis, LLM Research, Funding Research, Competition Analysis")
            
            # Run detailed research
            research_results = run_part_2(self.groq_api_key)
            
            if research_results:
                self.results['part2_researched'] = len(research_results)
                print(f"SUCCESS: Part 2 Complete - {len(research_results)} companies researched")
                
                # Show research quality metrics
                websites_found = len([r for r in research_results if r.get('website') and r['website'] != 'Unknown'])
                ai_chatbots = len([r for r in research_results if 'yes' in str(r.get('ai_powered_legal_chatbot', '')).lower()])
                german_market = len([r for r in research_results if 'german' in str(r.get('coverage', '')).lower()])
                
                print(f"   - Websites found: {websites_found}")
                print(f"   - AI chatbot companies: {ai_chatbots}")
                print(f"   - German market presence: {german_market}")
                
                return research_results
            else:
                print("ERROR: Part 2 failed to research companies")
                return None
                
        except Exception as e:
            print(f"ERROR: Part 2 - {e}")
            return None

    def run_part_3_with_monitoring(self):
        """Run Part 3 with progress monitoring"""
        try:
            print("\nPART 3: Excel Benchmark Export")
            print("-" * 40)
            print("CREATING: Main benchmark + Analysis sheets")
            
            # Run Excel export
            excel_success = run_part_3()
            
            if excel_success:
                self.results['part3_excel_created'] = True
                print("SUCCESS: Part 3 Complete - Professional Excel benchmark created")
                
                # Check if file was actually created
                if os.path.exists("Benchmark.xlsx"):
                    file_size = os.path.getsize("Benchmark.xlsx")
                    print(f"   - File: Benchmark.xlsx ({file_size:,} bytes)")
                    print("   - Sheets: Benchmark, Summary Analysis, Competitive Positioning, German Market Focus")
                else:
                    print("WARNING: Excel file not found after creation")
                
                return True
            else:
                print("ERROR: Part 3 failed to create Excel file")
                return False
                
        except Exception as e:
            print(f"ERROR: Part 3 - {e}")
            return False

    def calculate_final_results(self):
        """Calculate final research metrics"""
        end_time = datetime.now()
        self.results['total_time'] = (end_time - self.start_time).total_seconds()

    def print_final_summary(self):
        """Print comprehensive final summary"""
        print("\n" + "="*60)
        print("LEGAL TECH RESEARCH COMPLETE!")
        print("="*60)
        
        print(f"TOTAL EXECUTION TIME: {self.results['total_time']:.1f} seconds")
        print(f"COMPANIES DISCOVERED: {self.results['part1_companies']}")
        print(f"COMPANIES RESEARCHED: {self.results['part2_researched']}")
        print(f"EXCEL BENCHMARK: {'SUCCESS' if self.results['part3_excel_created'] else 'FAILED'}")
        
        # Research efficiency metrics
        if self.results['part1_companies'] > 0:
            research_rate = (self.results['part2_researched'] / self.results['part1_companies']) * 100
            print(f"RESEARCH COMPLETION RATE: {research_rate:.1f}%")
        
        print("\nDELIVERABLES:")
        print("   * discovered_companies.json - Raw company discovery data")
        print("   * company_research_results.json - Detailed research data") 
        print("   * Benchmark.xlsx - Professional competitive analysis")
        
        print("\nEXCEL SHEETS CREATED:")
        print("   1. Benchmark - Main competitor data table")
        print("   2. Summary Analysis - Key metrics and statistics")
        print("   3. Competitive Positioning - Threat assessment")
        print("   4. German Market Focus - Oratio-specific analysis")
        
        # Next steps recommendations
        print("\nRECOMMENDED NEXT STEPS:")
        print("   * Review Benchmark.xlsx for strategic insights")
        print("   * Focus on 'High' threat competitors in Competitive Positioning sheet")
        print("   * Analyze German Market Focus sheet for local competition")
        print("   * Use Comment column for strategic decision making")
        
        print("\nTO UPDATE DATA, RUN INDIVIDUAL PARTS:")
        print("   python part1_company_discovery.py  # Discover new companies")
        print("   python part2_company_research.py   # Research existing companies") 
        print("   python part3_excel_export.py       # Regenerate Excel file")

def main():
    """Main orchestrator entry point"""
    # Initialize orchestrator
    orchestrator = LegalTechResearchOrchestrator()
    
    # Run complete research pipeline
    success = orchestrator.run_complete_research()
    
    if success:
        print(f"\n>> Research pipeline completed successfully!")
        return 0
    else:
        print(f"\n>> Research pipeline failed. Check error messages above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)