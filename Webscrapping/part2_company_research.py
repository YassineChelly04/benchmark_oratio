"""
Legal Tech Competitor Research System - Part 2: Detailed Company Research
Using LLM and search agents with FREE APIs to gather comprehensive company information
"""

import json
import requests
from bs4 import BeautifulSoup
import time
import random
import re
import os
import feedparser
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote_plus, urljoin

class CompanyResearchAgent:
    def __init__(self, groq_api_key):
        self.groq_api_key = groq_api_key
        self.session = requests.Session()
        self.companies_data = {}
        self.research_results = []
        
        # Enhanced headers for web scraping
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        
        # Free API endpoints
        self.free_apis = {
            'duckduckgo': 'https://api.duckduckgo.com/',
            'google_news_rss': 'https://news.google.com/rss/search',
            'hacker_news': 'https://hn.algolia.com/api/v1/search',
            'opencorporates': 'https://api.opencorporates.com/v0.4/companies/search',
            'github': 'https://api.github.com'
        }

    def research_all_companies(self, companies_file="discovered_companies.json"):
        """Main method to research all discovered companies"""
        print("PART 2: Detailed Company Research")
        print("=" * 50)
        
        # Load companies from Part 1
        companies = self.load_companies_list(companies_file)
        
        if not companies:
            print("ERROR: No companies found to research")
            return
        
        print(f"Researching {len(companies)} companies...")
        
        # Research each company in detail
        for i, company in enumerate(companies):
            print(f"\nProgress: {i+1}/{len(companies)} - {company['name']}")
            
            try:
                # Multi-agent research approach
                company_profile = self.research_single_company(company)
                self.research_results.append(company_profile)
                
                # Rate limiting
                time.sleep(random.uniform(3, 6))
                
            except Exception as e:
                print(f"ERROR researching {company['name']}: {e}")
                continue
        
        # Save detailed research results
        self.save_research_results()
        return self.research_results

    def load_companies_list(self, filename):
        """Load companies list from Part 1"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    companies = json.load(f)
                print(f"SUCCESS: Loaded {len(companies)} companies from {filename}")
                return companies
            else:
                print(f"ERROR: File {filename} not found")
                return []
        except Exception as e:
            print(f"Error loading companies: {e}")
            return []

    def research_single_company(self, company):
        """Research a single company using multiple agents"""
        company_name = company['name']
        
        # Initialize company profile
        profile = {
            'competitor': company_name,
            'discovery_info': company,
            'research_timestamp': datetime.now().isoformat(),
            'website': '',
            'business_model': '',
            'ai_powered_legal_chatbot': '',
            'stage': '',
            'fundraising_stage': '',
            'multilingual_support': '',
            'mobile_web_accessibility': '',
            'api_integration': '',
            'free_tier': '',
            'subscription_based': '',
            'pricing': '',
            'target_audience': '',
            'user_base_growth_rate': '',
            'partnerships_integrations': '',
            'coverage': '',
            'product': '',
            'founding_team_rating': '',
            'direct_indirect': '',
            'comment': ''
        }
        
        # Agent 1: Web Search Agent
        search_data = self.web_search_agent(company_name)
        
        # Agent 2: Website Analysis Agent
        if search_data.get('website'):
            website_data = self.website_analysis_agent(search_data['website'])
            profile.update(website_data)
        
        # Agent 3: LLM Research Agent
        llm_data = self.llm_research_agent(company_name, search_data)
        profile.update(llm_data)
        
        # Agent 4: Funding Research Agent
        funding_data = self.funding_research_agent(company_name)
        profile.update(funding_data)
        
        # Agent 5: Competition Analysis Agent
        competition_data = self.competition_analysis_agent(company_name, search_data)
        profile.update(competition_data)
        
        return profile

    def web_search_agent(self, company_name):
        """Agent 1: Enhanced web search using multiple FREE APIs"""
        print(f"Enhanced Web Search Agent researching {company_name}")
        
        search_data = {
            'website': '',
            'search_results': '',
            'news_mentions': [],
            'github_activity': {},
            'corporate_data': {},
            'tech_mentions': []
        }
        
        # 1. DuckDuckGo Search (FREE, no rate limits)
        try:
            ddg_results = self.duckduckgo_search(company_name)
            search_data.update(ddg_results)
            print(f"  - DuckDuckGo: Found website and search data")
        except Exception as e:
            print(f"  - DuckDuckGo search error: {e}")
        
        # 2. Google News RSS (FREE)
        try:
            news_data = self.google_news_search(company_name)
            search_data['news_mentions'] = news_data
            print(f"  - Google News: Found {len(news_data)} recent articles")
        except Exception as e:
            print(f"  - Google News error: {e}")
        
        # 3. Hacker News API (FREE)
        try:
            hn_data = self.hacker_news_search(company_name)
            search_data['tech_mentions'] = hn_data
            print(f"  - Hacker News: Found {len(hn_data)} tech discussions")
        except Exception as e:
            print(f"  - Hacker News error: {e}")
        
        # 4. OpenCorporates API (FREE basic tier)
        try:
            corp_data = self.opencorporates_search(company_name)
            search_data['corporate_data'] = corp_data
            print(f"  - OpenCorporates: Found corporate registration data")
        except Exception as e:
            print(f"  - OpenCorporates error: {e}")
        
        # 5. GitHub API (FREE)
        try:
            github_data = self.github_search(company_name)
            search_data['github_activity'] = github_data
            print(f"  - GitHub: Found {github_data.get('repo_count', 0)} repositories")
        except Exception as e:
            print(f"  - GitHub error: {e}")
        
        # 6. Fallback to original Google scraping if needed
        if not search_data.get('website') and not search_data.get('search_results'):
            try:
                fallback_data = self.google_scraping_fallback(company_name)
                search_data.update(fallback_data)
                print(f"  - Google scraping fallback: Used as backup")
            except Exception as e:
                print(f"  - Fallback search error: {e}")
        
        # Compile comprehensive search results
        all_content = ""
        if search_data.get('search_results'):
            all_content += search_data['search_results'][:1000]
        
        # Add news content
        for article in search_data.get('news_mentions', [])[:3]:
            all_content += f" {article.get('title', '')} {article.get('description', '')}"[:500]
        
        # Add tech discussion content
        for discussion in search_data.get('tech_mentions', [])[:2]:
            all_content += f" {discussion.get('title', '')} {discussion.get('text', '')}"[:300]
        
        search_data['search_results'] = all_content
        return search_data

    def duckduckgo_search(self, company_name):
        """DuckDuckGo Instant Answer API - FREE with no rate limits"""
        search_data = {'website': '', 'search_results': ''}
        
        # DuckDuckGo Instant Answer API
        params = {
            'q': f"{company_name} legal tech",
            'format': 'json',
            'no_html': '1',
            'skip_disambig': '1'
        }
        
        response = self.session.get(self.free_apis['duckduckgo'], params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract website from official source
            if data.get('Infobox') and data['Infobox'].get('content'):
                for item in data['Infobox']['content']:
                    if item.get('label', '').lower() in ['website', 'official website', 'url']:
                        search_data['website'] = item.get('value', '')
                        break
            
            # Extract abstract/description
            if data.get('Abstract'):
                search_data['search_results'] = data['Abstract']
            
            # Extract definition if available
            if data.get('Definition'):
                search_data['search_results'] += f" {data['Definition']}"
            
            # Extract related topics
            if data.get('RelatedTopics'):
                related_text = ""
                for topic in data['RelatedTopics'][:3]:
                    if isinstance(topic, dict) and topic.get('Text'):
                        related_text += f" {topic['Text']}"
                search_data['search_results'] += related_text[:500]
        
        return search_data

    def google_news_search(self, company_name):
        """Google News RSS - FREE with no API key needed"""
        news_articles = []
        
        # Google News RSS search
        query = quote_plus(f"{company_name} legal tech startup funding")
        rss_url = f"{self.free_apis['google_news_rss']}?q={query}&hl=en-US&gl=US&ceid=US:en"
        
        try:
            # Parse RSS feed
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:5]:  # Get top 5 articles
                article = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'description': entry.get('summary', '')[:200],
                    'source': entry.get('source', {}).get('title', 'Google News')
                }
                news_articles.append(article)
                
        except Exception as e:
            print(f"Google News RSS parsing error: {e}")
        
        return news_articles

    def hacker_news_search(self, company_name):
        """Hacker News API - FREE search for tech discussions"""
        tech_discussions = []
        
        # Search Hacker News for company mentions
        params = {
            'query': company_name,
            'tags': 'story',
            'hitsPerPage': 5
        }
        
        try:
            response = self.session.get(self.free_apis['hacker_news'], params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                for hit in data.get('hits', []):
                    discussion = {
                        'title': hit.get('title', ''),
                        'url': hit.get('url', ''),
                        'points': hit.get('points', 0),
                        'num_comments': hit.get('num_comments', 0),
                        'created_at': hit.get('created_at', ''),
                        'text': hit.get('story_text', '')[:300] if hit.get('story_text') else '',
                        'hn_url': f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
                    }
                    tech_discussions.append(discussion)
                    
        except Exception as e:
            print(f"Hacker News API error: {e}")
        
        return tech_discussions

    def opencorporates_search(self, company_name):
        """OpenCorporates API - FREE basic tier for corporate data"""
        corporate_data = {}
        
        # Search for company registration data
        params = {
            'q': company_name,
            'format': 'json',
            'per_page': 3
        }
        
        try:
            response = self.session.get(self.free_apis['opencorporates'], params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('results') and data['results'].get('companies'):
                    companies = data['results']['companies']
                    
                    for company in companies[:2]:  # Check top 2 matches
                        company_data = company.get('company', {})
                        
                        # Look for exact or close matches
                        if self.is_company_match(company_name, company_data.get('name', '')):
                            corporate_data = {
                                'registered_name': company_data.get('name', ''),
                                'jurisdiction': company_data.get('jurisdiction_code', ''),
                                'incorporation_date': company_data.get('incorporation_date', ''),
                                'company_type': company_data.get('company_type', ''),
                                'status': company_data.get('current_status', ''),
                                'registered_address': company_data.get('registered_address_in_full', ''),
                                'opencorporates_url': company_data.get('opencorporates_url', '')
                            }
                            break
                            
        except Exception as e:
            print(f"OpenCorporates API error: {e}")
        
        return corporate_data

    def github_search(self, company_name):
        """GitHub API - FREE for repository and organization search"""
        github_data = {
            'repo_count': 0,
            'total_stars': 0,
            'languages': [],
            'recent_activity': [],
            'organization_url': '',
            'public_repos': []
        }
        
        try:
            # Search for repositories
            repo_params = {
                'q': company_name,
                'sort': 'stars',
                'per_page': 5
            }
            
            repo_response = self.session.get(f"{self.free_apis['github']}/search/repositories", 
                                          params=repo_params, timeout=10)
            
            if repo_response.status_code == 200:
                repo_data = repo_response.json()
                
                github_data['repo_count'] = repo_data.get('total_count', 0)
                
                for repo in repo_data.get('items', []):
                    github_data['total_stars'] += repo.get('stargazers_count', 0)
                    
                    if repo.get('language') and repo['language'] not in github_data['languages']:
                        github_data['languages'].append(repo['language'])
                    
                    github_data['public_repos'].append({
                        'name': repo.get('name', ''),
                        'description': repo.get('description', '')[:100] if repo.get('description') else '',
                        'stars': repo.get('stargazers_count', 0),
                        'language': repo.get('language', ''),
                        'updated': repo.get('updated_at', ''),
                        'url': repo.get('html_url', '')
                    })
            
            # Search for organizations
            time.sleep(1)  # Rate limiting
            org_params = {
                'q': f"{company_name} type:org",
                'per_page': 3
            }
            
            org_response = self.session.get(f"{self.free_apis['github']}/search/users", 
                                         params=org_params, timeout=10)
            
            if org_response.status_code == 200:
                org_data = org_response.json()
                
                for org in org_data.get('items', []):
                    if self.is_company_match(company_name, org.get('login', '')):
                        github_data['organization_url'] = org.get('html_url', '')
                        break
                        
        except Exception as e:
            print(f"GitHub API error: {e}")
        
        return github_data

    def is_company_match(self, search_name, found_name):
        """Check if found company name matches search name"""
        search_clean = re.sub(r'[^a-zA-Z0-9]', '', search_name.lower())
        found_clean = re.sub(r'[^a-zA-Z0-9]', '', found_name.lower())
        
        # Check for exact match or if one contains the other
        return (search_clean in found_clean or found_clean in search_clean or 
                abs(len(search_clean) - len(found_clean)) <= 3)

    def google_scraping_fallback(self, company_name):
        """Original Google scraping as fallback method"""
        search_data = {'website': '', 'search_results': ''}
        
        # Multiple search queries for comprehensive coverage
        search_queries = [
            f"{company_name} legal tech AI startup",
            f"{company_name} company website official"
        ]
        
        all_search_content = ""
        
        for query in search_queries[:2]:  # Limit to 2 queries for fallback
            try:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                response = self.session.get(search_url, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                    
                    # Extract website URL
                    if not search_data['website']:
                        search_data['website'] = self.extract_website_from_search(soup, company_name)
                    
                    # Collect search content
                    search_content = soup.get_text()
                    all_search_content += search_content[:1000]  # Limit content
                
                time.sleep(random.uniform(2, 4))  # Respectful delay
                
            except Exception as e:
                print(f"Fallback search error for '{query}': {e}")
                continue
        
        search_data['search_results'] = all_search_content
        return search_data

    def extract_website_from_search(self, soup, company_name):
        """Extract website URL from Google search results"""
        try:
            # Look for links that might be the company website
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                if href.startswith('/url?q='):
                    # Extract actual URL from Google redirect
                    actual_url = href.split('/url?q=')[1].split('&')[0]
                    
                    # Check if this looks like a company website
                    if any(term in actual_url.lower() for term in [company_name.lower().replace(' ', ''), '.com', '.org', '.net']):
                        return actual_url
            
            return ""
        except Exception as e:
            print(f"Website extraction error: {e}")
            return ""

    def website_analysis_agent(self, website_url):
        """Agent 2: Analyze company website for detailed information"""
        print(f"Website Analysis Agent analyzing {website_url}")
        
        website_data = {
            'website': website_url,
            'business_model': 'Unknown',
            'pricing': 'Unknown',
            'product': 'Unknown',
            'api_integration': 'Unknown'
        }
        
        try:
            response = self.session.get(website_url, timeout=20)
            if response.status_code == 200:
                # Fix encoding issues by specifying UTF-8
                soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                page_text = soup.get_text().lower()
                
                # Extract business model
                if any(term in page_text for term in ['saas', 'software as a service', 'subscription']):
                    website_data['business_model'] = 'SaaS'
                elif any(term in page_text for term in ['marketplace', 'platform']):
                    website_data['business_model'] = 'Platform'
                elif any(term in page_text for term in ['consulting', 'services']):
                    website_data['business_model'] = 'Services'
                
                # Extract pricing information
                pricing_patterns = [r'€\d+', r'\$\d+', r'£\d+', r'\d+/month', r'\d+/year']
                for pattern in pricing_patterns:
                    matches = re.findall(pattern, page_text)
                    if matches:
                        website_data['pricing'] = ', '.join(matches[:3])
                        break
                
                # Check for API
                if any(term in page_text for term in ['api', 'developer', 'integration']):
                    website_data['api_integration'] = 'Yes'
                
                # Extract product description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    website_data['product'] = meta_desc.get('content', '')[:200]
                
        except Exception as e:
            print(f"Website analysis error: {e}")
        
        return website_data

    def llm_research_agent(self, company_name, search_data):
        """Agent 3: Enhanced LLM analysis with FREE API data"""
        print(f"LLM Research Agent analyzing {company_name}")
        
        # Enhanced prompt with FREE API data
        enhanced_context = f"""
Company Name: {company_name}

=== SEARCH RESULTS ===
{search_data.get('search_results', '')[:2000]}

=== RECENT NEWS ===
"""
        
        # Add news context
        for article in search_data.get('news_mentions', [])[:3]:
            enhanced_context += f"- {article.get('title', '')}: {article.get('description', '')}\n"
        
        enhanced_context += "\n=== TECH COMMUNITY DISCUSSIONS ===\n"
        
        # Add Hacker News context
        for discussion in search_data.get('tech_mentions', [])[:2]:
            enhanced_context += f"- HN: {discussion.get('title', '')} ({discussion.get('points', 0)} points)\n"
        
        enhanced_context += "\n=== CORPORATE DATA ===\n"
        corp_data = search_data.get('corporate_data', {})
        if corp_data:
            enhanced_context += f"Registered: {corp_data.get('registered_name', '')}\n"
            enhanced_context += f"Jurisdiction: {corp_data.get('jurisdiction', '')}\n"
            enhanced_context += f"Status: {corp_data.get('status', '')}\n"
        
        enhanced_context += "\n=== GITHUB ACTIVITY ===\n"
        github_data = search_data.get('github_activity', {})
        if github_data.get('repo_count', 0) > 0:
            enhanced_context += f"Repositories: {github_data.get('repo_count', 0)}\n"
            enhanced_context += f"Total Stars: {github_data.get('total_stars', 0)}\n"
            enhanced_context += f"Languages: {', '.join(github_data.get('languages', []))}\n"
        
        # Prepare comprehensive prompt for LLM
        research_prompt = f"""
You are a legal technology market research analyst. Analyze the company "{company_name}" using the comprehensive data below and provide detailed information.

{enhanced_context}

Website: {search_data.get('website', '')}

Provide a JSON response with these fields:
{{
    "ai_powered_legal_chatbot": "Yes/No/Limited - specify AI chatbot capabilities",
    "stage": "Pre-seed/Seed/Series A/B/C/Growth/Established",
    "multilingual_support": "Languages supported (German/English/etc)",
    "mobile_web_accessibility": "Mobile app/Web/Both availability",
    "free_tier": "Yes/No - free offering details",
    "subscription_based": "Yes/No - subscription model",
    "target_audience": "Law firms/Individuals/Corporates/SMEs",
    "coverage": "Geographic coverage (Germany/Europe/Global)",
    "founding_team_rating": "1-5 rating based on experience",
    "direct_indirect": "Direct/Indirect competitor to German legal chatbot",
    "comment": "Key insights and competitive positioning including recent news and tech community sentiment"
}}

Focus on accuracy and German legal tech market relevance. Use the news, discussions, and corporate data to provide current insights. Only respond with valid JSON.
"""
        
        try:
            llm_response = self.call_groq_llm(research_prompt)
            if llm_response:
                # Parse JSON response
                llm_data = json.loads(llm_response)
                return llm_data
        except Exception as e:
            print(f"LLM research error: {e}")
        
        # Enhanced fallback with FREE API data
        print(f"Using enhanced fallback analysis for {company_name}")
        return self.enhanced_fallback_analysis(company_name, search_data)

    def enhanced_fallback_analysis(self, company_name, search_data):
        """Enhanced fallback analysis using FREE API data"""
        company_lower = company_name.lower()
        search_text = search_data.get('search_results', '').lower()
        
        # Basic rule-based analysis
        fallback_data = {
            'ai_powered_legal_chatbot': 'Unknown',
            'stage': 'Unknown',
            'multilingual_support': 'Unknown',
            'mobile_web_accessibility': 'Unknown',
            'free_tier': 'Unknown',
            'subscription_based': 'Unknown',
            'target_audience': 'Unknown',
            'coverage': 'Unknown',
            'founding_team_rating': '3',
            'direct_indirect': 'Unknown',
            'comment': f'Enhanced analysis using FREE APIs for {company_name}'
        }
        
        # Enhanced AI chatbot detection using multiple sources
        ai_indicators = 0
        
        # Check company name
        if any(term in company_lower for term in ['ai', 'chatbot', 'assistant', 'gpt', 'bot']):
            ai_indicators += 2
        
        # Check search results
        if any(term in search_text for term in ['artificial intelligence', 'machine learning', 'nlp', 'chatbot']):
            ai_indicators += 1
        
        # Check news mentions
        for article in search_data.get('news_mentions', []):
            article_text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            if any(term in article_text for term in ['ai', 'artificial intelligence', 'chatbot']):
                ai_indicators += 1
                break
        
        # Check GitHub activity for AI-related repositories
        github_data = search_data.get('github_activity', {})
        for repo in github_data.get('public_repos', []):
            repo_text = f"{repo.get('name', '')} {repo.get('description', '')}".lower()
            if any(term in repo_text for term in ['ai', 'ml', 'nlp', 'chatbot', 'assistant']):
                ai_indicators += 1
                break
        
        # Determine AI capability based on indicators
        if ai_indicators >= 3:
            fallback_data['ai_powered_legal_chatbot'] = 'Yes - multiple AI indicators found'
        elif ai_indicators >= 1:
            fallback_data['ai_powered_legal_chatbot'] = 'Possible - some AI indicators found'
        else:
            fallback_data['ai_powered_legal_chatbot'] = 'No - no clear AI indicators'
        
        # Enhanced stage detection using news and corporate data
        corp_data = search_data.get('corporate_data', {})
        recent_news = search_data.get('news_mentions', [])
        
        # Check for funding news
        funding_found = False
        for article in recent_news:
            article_text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            if any(term in article_text for term in ['funding', 'investment', 'series', 'raised', 'venture']):
                if 'series c' in article_text or 'series d' in article_text:
                    fallback_data['stage'] = 'Established'
                elif 'series a' in article_text or 'series b' in article_text:
                    fallback_data['stage'] = 'Growth'
                elif 'seed' in article_text:
                    fallback_data['stage'] = 'Startup'
                funding_found = True
                break
        
        if not funding_found and corp_data.get('incorporation_date'):
            # Estimate stage based on incorporation date
            try:
                inc_year = int(corp_data['incorporation_date'][:4])
                current_year = 2025
                years_active = current_year - inc_year
                
                if years_active >= 8:
                    fallback_data['stage'] = 'Established'
                elif years_active >= 4:
                    fallback_data['stage'] = 'Growth'
                else:
                    fallback_data['stage'] = 'Startup'
            except:
                pass
        
        # Enhanced geographic coverage detection
        coverage_indicators = []
        
        # Check corporate jurisdiction
        if corp_data.get('jurisdiction'):
            jurisdiction = corp_data['jurisdiction'].lower()
            if 'de' in jurisdiction or 'german' in jurisdiction:
                coverage_indicators.append('Germany')
            elif any(eu_code in jurisdiction for eu_code in ['gb', 'fr', 'es', 'it', 'nl']):
                coverage_indicators.append('Europe')
            elif 'us' in jurisdiction:
                coverage_indicators.append('Global/US')
        
        # Check all text sources for geographic mentions
        all_text = f"{search_text} {' '.join([a.get('title', '') + ' ' + a.get('description', '') for a in recent_news])}"
        
        if any(term in all_text for term in ['german', 'germany', 'deutsch']):
            coverage_indicators.append('Germany')
        elif any(term in all_text for term in ['europe', 'european', 'eu']):
            coverage_indicators.append('Europe')
        elif any(term in all_text for term in ['global', 'worldwide', 'international']):
            coverage_indicators.append('Global')
        
        if coverage_indicators:
            fallback_data['coverage'] = '/'.join(list(set(coverage_indicators)))
        
        # Enhanced comment with insights from FREE APIs
        comment_parts = []
        
        if recent_news:
            comment_parts.append(f"Recent news: {len(recent_news)} articles found")
        
        if github_data.get('repo_count', 0) > 0:
            comment_parts.append(f"GitHub: {github_data['repo_count']} repositories, {github_data.get('total_stars', 0)} stars")
        
        if corp_data:
            comment_parts.append(f"Registered in {corp_data.get('jurisdiction', 'unknown jurisdiction')}")
        
        tech_discussions = search_data.get('tech_mentions', [])
        if tech_discussions:
            total_points = sum(d.get('points', 0) for d in tech_discussions)
            comment_parts.append(f"HN discussions: {len(tech_discussions)} posts, {total_points} total points")
        
        if comment_parts:
            fallback_data['comment'] += f". Additional insights: {'; '.join(comment_parts)}"
        
        return fallback_data

    def call_groq_llm(self, prompt, retries=3):
        """Call Groq LLM API with improved retry logic and error handling"""
        for attempt in range(retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "model": "deepseek-r1-distill-llama-70b",
                    "messages": [
                        {"role": "system", "content": "You are a legal technology market research analyst. Provide accurate, detailed analysis in valid JSON format only."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.1,
                    "max_tokens": 2000
                }
                
                # Add connection timeout and read timeout
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=(30, 90)  # (connection timeout, read timeout)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # Validate JSON response
                    try:
                        json.loads(content)  # Test if it's valid JSON
                        return content
                    except json.JSONDecodeError:
                        print(f"LLM returned invalid JSON on attempt {attempt + 1}")
                        if attempt < retries - 1:
                            time.sleep(5)
                            continue
                        else:
                            return None
                            
                elif response.status_code == 429:
                    wait_time = (2 ** attempt) * 15  # Longer exponential backoff
                    print(f"Rate limited, waiting {wait_time} seconds... (attempt {attempt + 1})")
                    time.sleep(wait_time)
                elif response.status_code == 401:
                    print(f"Authentication error - check API key")
                    return None
                elif response.status_code >= 500:
                    print(f"Server error {response.status_code}, retrying...")
                    time.sleep(10)
                else:
                    print(f"API error: {response.status_code} - {response.text}")
                    return None
                    
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error on attempt {attempt + 1}: {e}")
                if attempt < retries - 1:
                    wait_time = (2 ** attempt) * 10
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached. Skipping LLM analysis for this company.")
                    return None
                    
            except requests.exceptions.Timeout as e:
                print(f"Timeout error on attempt {attempt + 1}: {e}")
                if attempt < retries - 1:
                    time.sleep(10)
                else:
                    return None
                    
            except Exception as e:
                print(f"Unexpected LLM call error (attempt {attempt+1}): {e}")
                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    return None
        
        return None

    def funding_research_agent(self, company_name):
        """Agent 4: Research funding and investment information"""
        print(f"Funding Research Agent analyzing {company_name}")
        
        funding_data = {
            'fundraising_stage': 'Unknown',
            'stage': 'Unknown'
        }
        
        # Search for funding information
        funding_queries = [
            f"{company_name} funding series venture capital raised",
            f"{company_name} investment round crunchbase",
            f"{company_name} valuation startup funding"
        ]
        
        for query in funding_queries:
            try:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                response = self.session.get(search_url, timeout=15)
                
                if response.status_code == 200:
                    # Fix encoding issues by specifying UTF-8
                    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                    text_content = soup.get_text().lower()
                    
                    # Extract funding stage
                    if 'series a' in text_content:
                        funding_data['fundraising_stage'] = 'Series A'
                        funding_data['stage'] = 'Growth'
                    elif 'series b' in text_content:
                        funding_data['fundraising_stage'] = 'Series B'
                        funding_data['stage'] = 'Growth'
                    elif 'series c' in text_content:
                        funding_data['fundraising_stage'] = 'Series C'
                        funding_data['stage'] = 'Established'
                    elif 'seed' in text_content:
                        funding_data['fundraising_stage'] = 'Seed'
                        funding_data['stage'] = 'Startup'
                    elif 'pre-seed' in text_content:
                        funding_data['fundraising_stage'] = 'Pre-seed'
                        funding_data['stage'] = 'Startup'
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"Funding search error: {e}")
                continue
        
        return funding_data

    def competition_analysis_agent(self, company_name, search_data):
        """Agent 5: Analyze competition and market positioning"""
        print(f"Competition Analysis Agent analyzing {company_name}")
        
        competition_data = {
            'partnerships_integrations': 'Unknown',
            'user_base_growth_rate': 'Unknown'
        }
        
        # Search for partnerships and user metrics
        partnership_queries = [
            f"{company_name} partnerships integrations customers",
            f"{company_name} users growth metrics statistics"
        ]
        
        for query in partnership_queries:
            try:
                search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                response = self.session.get(search_url, timeout=15)
                
                if response.status_code == 200:
                    # Fix encoding issues by specifying UTF-8
                    soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')
                    text_content = soup.get_text()
                    
                    # Extract partnerships
                    partnership_patterns = [
                        r'partnership with (\w+)',
                        r'integrates with (\w+)',
                        r'partners include (\w+)'
                    ]
                    
                    partnerships = []
                    for pattern in partnership_patterns:
                        matches = re.findall(pattern, text_content, re.IGNORECASE)
                        partnerships.extend(matches[:3])
                    
                    if partnerships:
                        competition_data['partnerships_integrations'] = ', '.join(partnerships)
                    
                    # Extract user metrics
                    user_patterns = [
                        r'(\d+(?:,\d{3})*)\s+users',
                        r'(\d+(?:,\d{3})*)\s+customers',
                        r'(\d+)%\s+growth'
                    ]
                    
                    for pattern in user_patterns:
                        matches = re.findall(pattern, text_content)
                        if matches:
                            competition_data['user_base_growth_rate'] = ', '.join(matches[:2])
                            break
                
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                print(f"Competition analysis error: {e}")
                continue
        
        return competition_data

    def save_research_results(self):
        """Save detailed research results to JSON file"""
        output_file = "company_research_results.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.research_results, f, indent=2, ensure_ascii=False)
            
            print(f"\nSUCCESS: Saved detailed research for {len(self.research_results)} companies to {output_file}")
            
            # Print summary
            successful_research = len([r for r in self.research_results if r.get('website')])
            print(f"Research Summary:")
            print(f"  Total companies researched: {len(self.research_results)}")
            print(f"  Companies with websites found: {successful_research}")
            print(f"  Research completion rate: {successful_research/len(self.research_results)*100:.1f}%")
            
        except Exception as e:
            print(f"Error saving research results: {e}")

def run_part_2(groq_api_key="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"):
    """Run Part 2: Detailed Company Research"""
    research_agent = CompanyResearchAgent(groq_api_key)
    results = research_agent.research_all_companies()
    return results

if __name__ == "__main__":
    run_part_2()