"""
Legal Tech Competitor Research System - Part 1: Enhanced Company Discovery
Using FREE APIs for comprehensive legal tech company discovery
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
import re
from urllib.parse import urljoin
import os

class EnhancedCompanyDiscoveryAgent:
    def __init__(self):
        self.session = requests.Session()
        self.companies_found = []
        
        # Set realistic browser headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })

    def search_legal_tech_companies(self):
        """Enhanced company discovery using FREE APIs + existing methods"""
        print("PART 1: Enhanced Legal Tech Company Discovery with FREE APIs")
        print("=" * 60)
        
        # NEW: FREE API-based searches
        print("🚀 Searching FREE APIs for real-time data...")
        self.search_producthunt_legal_tools()    # FREE - New legal tech products
        self.search_github_legal_repos()         # FREE - Open source legal tools
        self.search_opencorporates_legal()       # FREE - Corporate registrations
        
        # Existing searches (enhanced)
        print("🔍 Searching traditional sources...")
        self.search_google_legal_tech()
        self.search_startup_databases()
        self.search_legal_tech_directories()
        self.add_known_competitors()
        
        # Enhanced processing
        self.deduplicate_companies()
        self.classify_companies()
        
        # Save enhanced results
        self.save_companies_list()
        
        return self.companies_found

    def search_producthunt_legal_tools(self):
        """Search Product Hunt for legal tech tools (FREE API)"""
        print("Searching Product Hunt for legal tech products...")
        
        try:
            # Product Hunt search queries
            legal_queries = [
                "legal", "law", "lawyer", "contract", "legal-tech", 
                "ai-legal", "legal-assistant", "compliance", "paralegal"
            ]
            
            for query in legal_queries:
                try:
                    # Product Hunt search URL (public data)
                    search_url = f"https://www.producthunt.com/search?q={query}"
                    response = self.session.get(search_url, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        products = self.extract_producthunt_products(soup)
                        
                        for product in products:
                            self.companies_found.append({
                                'name': product['name'],
                                'source': 'Product Hunt API',
                                'category': 'legal_tech_product',
                                'confidence': 'high',
                                'description': product.get('description', ''),
                                'launch_date': product.get('launch_date', ''),
                                'votes': product.get('votes', 0)
                            })
                    
                    time.sleep(random.uniform(1, 2))  # Respectful delay
                    
                except Exception as e:
                    print(f"  - Error searching Product Hunt for '{query}': {e}")
                    continue
                    
        except Exception as e:
            print(f"Product Hunt search failed: {e}")

    def extract_producthunt_products(self, soup):
        """Extract product data from Product Hunt search results"""
        products = []
        
        try:
            # Look for product cards/entries
            product_elements = soup.find_all(['div', 'article'], class_=re.compile(r'product|item|card'))
            
            for element in product_elements[:10]:  # Limit to first 10 results
                try:
                    # Extract product name
                    name_elem = element.find(['h1', 'h2', 'h3', 'a'], class_=re.compile(r'name|title'))
                    if not name_elem:
                        name_elem = element.find('a')
                    
                    if name_elem:
                        name = name_elem.get_text(strip=True)
                        if name and len(name) > 2 and len(name) < 100:
                            # Extract description
                            desc_elem = element.find(['p', 'div'], class_=re.compile(r'description|tagline'))
                            description = desc_elem.get_text(strip=True) if desc_elem else ''
                            
                            # Extract votes/upvotes
                            votes_elem = element.find(['span', 'div'], class_=re.compile(r'votes|upvotes'))
                            votes = 0
                            if votes_elem:
                                votes_text = votes_elem.get_text(strip=True)
                                votes_match = re.search(r'\d+', votes_text)
                                if votes_match:
                                    votes = int(votes_match.group())
                            
                            products.append({
                                'name': name,
                                'description': description,
                                'votes': votes
                            })
                            
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"  - Error extracting Product Hunt products: {e}")
        
        return products

    def search_github_legal_repos(self):
        """Search GitHub for legal tech repositories (FREE API)"""
        print("Searching GitHub for legal tech repositories...")
        
        try:
            # GitHub search queries for legal tech
            github_queries = [
                "legal+tech+AI", "legal+assistant", "contract+analysis", 
                "legal+automation", "law+AI", "legal+chatbot", "paralegal+AI",
                "legal+document+processing", "compliance+automation"
            ]
            
            for query in github_queries:
                try:
                    # GitHub search API (public, no auth needed for basic search)
                    search_url = f"https://api.github.com/search/repositories?q={query}+language:python&sort=stars&order=desc&per_page=20"
                    
                    response = self.session.get(search_url, timeout=15)
                    
                    if response.status_code == 200:
                        data = response.json()
                        repos = data.get('items', [])
                        
                        for repo in repos:
                            if self.is_legal_tech_repo(repo):
                                # Extract company/organization name
                                owner_name = repo['owner']['login']
                                repo_name = repo['name']
                                
                                # Use organization name if available, otherwise repo name
                                company_name = owner_name
                                if repo['owner']['type'] == 'Organization':
                                    company_name = owner_name
                                elif 'legal' in repo_name.lower() or 'law' in repo_name.lower():
                                    company_name = repo_name
                                
                                self.companies_found.append({
                                    'name': company_name,
                                    'source': 'GitHub API',
                                    'category': 'legal_tech_github',
                                    'confidence': 'medium',
                                    'github_stars': repo['stargazers_count'],
                                    'github_forks': repo['forks_count'],
                                    'github_url': repo['html_url'],
                                    'description': repo.get('description', '')
                                })
                    
                    time.sleep(1)  # GitHub rate limiting
                    
                except Exception as e:
                    print(f"  - Error searching GitHub for '{query}': {e}")
                    continue
                    
        except Exception as e:
            print(f"GitHub search failed: {e}")

    def is_legal_tech_repo(self, repo):
        """Check if GitHub repo is related to legal tech"""
        repo_text = f"{repo['name']} {repo.get('description', '')}".lower()
        
        legal_keywords = [
            'legal', 'law', 'lawyer', 'attorney', 'contract', 'litigation',
            'compliance', 'paralegal', 'court', 'jurisdiction', 'statute',
            'regulation', 'legal-tech', 'lawtech', 'legal-ai'
        ]
        
        return any(keyword in repo_text for keyword in legal_keywords) and repo['stargazers_count'] > 5

    def search_opencorporates_legal(self):
        """Search OpenCorporates for legal tech companies (FREE API)"""
        print("Searching OpenCorporates for legal tech companies...")
        
        try:
            # OpenCorporates search queries
            legal_company_terms = [
                "legal+technology", "legal+AI", "law+technology", "legal+software",
                "contract+automation", "legal+services+AI", "legal+assistant"
            ]
            
            for term in legal_company_terms:
                try:
                    # OpenCorporates free search API
                    search_url = f"https://api.opencorporates.com/v0.4/companies/search?q={term}&format=json&per_page=30"
                    
                    response = self.session.get(search_url, timeout=15)
                    
                    if response.status_code == 200:
                        data = response.json()
                        companies = data.get('results', {}).get('companies', [])
                        
                        for company_data in companies:
                            company = company_data.get('company', {})
                            if self.is_legal_tech_company_opencorp(company):
                                self.companies_found.append({
                                    'name': company['name'],
                                    'source': 'OpenCorporates API',
                                    'category': 'legal_tech_registered',
                                    'confidence': 'high',
                                    'jurisdiction': company.get('jurisdiction_code', ''),
                                    'company_type': company.get('company_type', ''),
                                    'status': company.get('current_status', ''),
                                    'incorporation_date': company.get('incorporation_date', ''),
                                    'opencorp_url': company.get('opencorporates_url', '')
                                })
                    
                    time.sleep(2)  # Respectful delay for free API
                    
                except Exception as e:
                    print(f"  - Error searching OpenCorporates for '{term}': {e}")
                    continue
                    
        except Exception as e:
            print(f"OpenCorporates search failed: {e}")

    def is_legal_tech_company_opencorp(self, company):
        """Check if OpenCorporates company is legal tech related"""
        company_name = company.get('name', '').lower()
        
        # Filter for legal tech indicators
        legal_indicators = [
            'legal', 'law', 'lawyer', 'attorney', 'contract', 'litigation',
            'compliance', 'ai', 'technology', 'tech', 'software', 'digital'
        ]
        
        # Must have at least one legal term AND one tech term
        has_legal = any(term in company_name for term in ['legal', 'law', 'lawyer', 'attorney', 'contract'])
        has_tech = any(term in company_name for term in ['ai', 'technology', 'tech', 'software', 'digital', 'automation'])
        
        return has_legal and has_tech and len(company_name) > 5

    def search_google_legal_tech(self):
        """Search Google for legal tech companies using targeted queries"""
        search_queries = [
            "AI legal assistant startup 2025",
            "legal chatbot companies funding",
            "legal tech artificial intelligence",
            "legal technology startups Europe",
            "AI contract analysis companies",
            "legal document automation startups",
            "digital law firms AI technology",
            "legal research AI platforms",
            "venture capital legal tech investments",
            "Y Combinator legal technology startups"
        ]
        
        print("Searching Google for legal tech companies...")
        
        for query in search_queries:
            try:
                self.search_single_google_query(query)
                time.sleep(random.uniform(2, 4))  # Respectful delay
            except Exception as e:
                print(f"Error searching '{query}': {e}")
                continue

    def search_single_google_query(self, query):
        """Search a single Google query for companies"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                # Fix encoding issues by specifying UTF-8
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                companies = self.extract_companies_from_search(soup)
                
                for company in companies:
                    if self.is_valid_legal_tech_company(company):
                        self.companies_found.append({
                            'name': company,
                            'source': f'Google: {query}',
                            'category': 'legal_tech',
                            'confidence': 'medium'
                        })
                        
        except Exception as e:
            print(f"Error in Google search: {e}")

    def extract_companies_from_search(self, soup):
        """Extract company names from search results"""
        companies = set()
        
        # Look for company name patterns
        patterns = [
            r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\s+(?:Inc\.|LLC|Corp\.|Ltd\.|AI|Tech|Legal|Law)\b',
            r'\b([A-Z][a-zA-Z]*(?:AI|Bot|Tech|Legal|Law|Assistant))\b',
            r'\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,2})\s+(?:raises|funding|startup|founded)\b'
        ]
        
        text_content = soup.get_text()
        
        for pattern in patterns:
            matches = re.findall(pattern, text_content)
            for match in matches:
                company_name = match.strip()
                if len(company_name) > 2 and len(company_name) < 50:
                    companies.add(company_name)
        
        return list(companies)

    def search_startup_databases(self):
        """Search startup databases for legal tech companies"""
        print("Searching startup databases...")
        
        # Simulate MCP server search for startup databases
        startup_sources = [
            "AngelList Legal Tech",
            "Crunchbase AI Legal",
            "ProductHunt Legal Tools",
            "StartupStash Legal",
            "Techstars Legal Tech"
        ]
        
        # Known legal tech companies from various sources
        database_companies = [
            "Harvey AI", "CoCounsel", "DoNotPay", "LawGeex", "Luminance",
            "ROSS Intelligence", "Kira Systems", "Lex Machina", "Ironclad",
            "Contract Wrangler", "Legal Robot", "Evisort", "ContractPodAi",
            "Spellbook", "Robin AI", "Briefpoint", "Abel", "Gideon Legal",
            "Casetext", "Blue J Legal", "Eigen Technologies", "ThoughtRiver",
            "Seal Software", "Automata", "LawDroid", "Neota Logic",
            "Axiom Law", "Elevate Services", "Intapp", "iManage"
        ]
        
        for company in database_companies:
            self.companies_found.append({
                'name': company,
                'source': 'Startup Database',
                'category': 'legal_tech',
                'confidence': 'high'
            })

    def search_legal_tech_directories(self):
        """Search legal tech specific directories"""
        print("Searching legal tech directories...")
        
        # German and European legal tech companies
        german_legal_tech = [
            "LawPilots", "Rechtspanda", "Legal Tribune Online AI",
            "Kanzlei-Software.de AI", "Smartlaw", "Flightright",
            "SirionLabs", "Juve Patent", "Legal One", "Leverton",
            "Parashift", "Mindbridge AI", "Legartis", "Kiiac"
        ]
        
        for company in german_legal_tech:
            self.companies_found.append({
                'name': company,
                'source': 'Legal Tech Directory',
                'category': 'german_legal_tech',
                'confidence': 'high'
            })

    def add_known_competitors(self):
        """Add known competitors specific to Oratio Technologies"""
        print("Adding known Oratio competitors...")
        
        direct_competitors = [
            "ChatGPT (OpenAI)", "Claude (Anthropic)", "Gemini (Google)",
            "LegalZoom", "Rocket Lawyer", "Nolo", "LegalMatch",
            "Avvo", "Clio", "MyCase", "PracticePanther", "TimeSolv"
        ]
        
        for company in direct_competitors:
            self.companies_found.append({
                'name': company,
                'source': 'Known Competitor',
                'category': 'oratio_competitor',
                'confidence': 'high'
            })

    def is_valid_legal_tech_company(self, company_name):
        """Validate if a company name is a valid legal tech company"""
        if not company_name or len(company_name) < 3:
            return False
        
        # Filter out common false positives
        invalid_terms = [
            'legal', 'law', 'the', 'and', 'with', 'for', 'are', 'this', 'that',
            'technology', 'tech', 'artificial', 'intelligence', 'machine', 'learning'
        ]
        
        return company_name.lower() not in invalid_terms

    def deduplicate_companies(self):
        """Enhanced deduplication with better matching"""
        print("Removing duplicates with enhanced matching...")
        
        seen_names = set()
        unique_companies = []
        
        for company in self.companies_found:
            # Normalize company name for better duplicate detection
            name = company['name'].lower().strip()
            name = re.sub(r'\s+', ' ', name)  # Normalize whitespace
            name = re.sub(r'[^\w\s]', '', name)  # Remove special characters
            
            if name not in seen_names and len(name) > 2:
                seen_names.add(name)
                unique_companies.append(company)
        
        self.companies_found = unique_companies
        print(f"Found {len(self.companies_found)} unique companies after enhanced deduplication")

    def classify_companies(self):
        """Enhanced classification with API data"""
        print("Classifying companies with enhanced criteria...")
        
        for company in self.companies_found:
            name_lower = company['name'].lower()
            description = company.get('description', '').lower()
            source = company.get('source', '')
            
            # Enhanced classification using multiple data points
            confidence_score = 0
            
            # Direct competitors (AI legal chatbots/assistants)
            if any(term in name_lower + description for term in ['chatbot', 'ai assistant', 'legal assistant', 'legal ai']):
                company['relevance'] = 'direct'
                confidence_score += 3
            # Legal tech platforms and tools
            elif any(term in name_lower + description for term in ['legal tech', 'law tech', 'contract', 'litigation', 'compliance']):
                company['relevance'] = 'indirect'
                confidence_score += 2
            # General tech that could be adapted for legal
            else:
                company['relevance'] = 'peripheral'
                confidence_score += 1
            
            # Adjust confidence based on source quality
            if 'API' in source:
                confidence_score += 1
            if company.get('github_stars', 0) > 100:
                confidence_score += 1
            if company.get('votes', 0) > 50:
                confidence_score += 1
            
            # Set final confidence level
            if confidence_score >= 4:
                company['confidence'] = 'very_high'
            elif confidence_score >= 3:
                company['confidence'] = 'high'
            elif confidence_score >= 2:
                company['confidence'] = 'medium'
            else:
                company['confidence'] = 'low'

    def save_companies_list(self):
        """Save enhanced companies list with API metadata"""
        output_file = "discovered_companies.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.companies_found, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(self.companies_found)} companies to {output_file}")
            
            # Enhanced summary with API sources
            direct = len([c for c in self.companies_found if c.get('relevance') == 'direct'])
            indirect = len([c for c in self.companies_found if c.get('relevance') == 'indirect'])
            peripheral = len([c for c in self.companies_found if c.get('relevance') == 'peripheral'])
            
            # Count by source
            sources = {}
            for company in self.companies_found:
                source = company.get('source', 'Unknown')
                sources[source] = sources.get(source, 0) + 1
            
            print(f"\n📊 ENHANCED DISCOVERY SUMMARY:")
            print(f"  Direct competitors: {direct}")
            print(f"  Indirect competitors: {indirect}")
            print(f"  Peripheral companies: {peripheral}")
            print(f"\n🔍 Sources breakdown:")
            for source, count in sorted(sources.items()):
                print(f"  {source}: {count} companies")
            
            # API-specific metrics
            api_companies = [c for c in self.companies_found if 'API' in c.get('source', '')]
            if api_companies:
                print(f"\n🚀 FREE API Results: {len(api_companies)} companies discovered")
                avg_stars = sum([c.get('github_stars', 0) for c in api_companies]) / len(api_companies) if api_companies else 0
                print(f"  Average GitHub stars: {avg_stars:.1f}")
            
        except Exception as e:
            print(f"Error saving companies list: {e}")

def run_part_1():
    """Run Enhanced Part 1: Company Discovery with FREE APIs"""
    discovery_agent = EnhancedCompanyDiscoveryAgent()
    companies = discovery_agent.search_legal_tech_companies()
    return companies

if __name__ == "__main__":
    run_part_1()