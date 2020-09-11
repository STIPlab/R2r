# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 19:49:07 2020

@author: Barreneche_A

REQUIRES conda install -c bokeh bokeh
"""

import pandas as pd
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, LinearAxis, OpenURL, TapTool, HBar
from bokeh.models.callbacks import CustomJS
from bokeh.events import Tap
from bokeh.models.tools import HoverTool

import nltk

def main(PAREA, THEMES):
    for i, item in enumerate(PAREA):
        Fig1(PAREA[i], THEMES[i])
        Fig2(PAREA[i], THEMES[i])
        Fig3(PAREA[i], THEMES[i])
        Fig4(PAREA[i], THEMES[i]) 
        Fig5(PAREA[i], THEMES[i])
         
def Fig1(parea, themes):

    writeTo = "templates/figures/" + parea + "/Figure1.html"
    
    output_file(writeTo, mode="inline")
    #NOTE: mode attribute to run output from a local file. In theory, it can be removed for an online file...
    
    #load online stip compass data using pipe '|' separator and skipping the second header (multi-indexing causes problems in the filtering)
    #url = 'https://stip.oecd.org/assets/downloads/STIP_Survey.csv'
    url = 'INPUT/STIP-Data-Flatcsv-Apr2020.csv'
    
    head_df = pd.read_csv(url, sep='|', nrows=1)
    themes_df = head_df[themes]
    themes_df = themes_df.T
    themes_df.rename(columns={0: "THlabel"}, inplace=True)
    
    compass_df = pd.read_csv(url, sep='|', skiprows=[1])
    d = ['EGY', 'IDN', 'IND', 'MAR', 'MYS', 'SAU', 'SGL', 'SRB', 'URY', 'VNM']
    compass_df = compass_df[~compass_df['CountryCode'].isin(d)]
    compass_df.drop_duplicates(subset = "InitiativeID", inplace=True)
    compass_df.Tags.fillna("¬", inplace=True)

    compass_df['theme'] = ""
    Fig1_df = pd.DataFrame(columns = compass_df.columns)
    
    for th in themes:
        compass_df.loc[compass_df[th] == "1", th] = 1
        compass_df.loc[compass_df[th] == 1, 'theme'] = themes_df.loc[th].values[0]
        Fig1_df = pd.concat([Fig1_df, compass_df[compass_df[th] == 1]])
    
    Fig1_df['count'] = 1
    
    grouped = Fig1_df.groupby('theme')[['count', 'HasBeenEvaluated']].sum()
    
    groupedkw = Fig1_df.groupby('theme')['Tags'].apply(lambda x: nltk.FreqDist(nltk.tokenize.regexp_tokenize('¬'.join(x), pattern='¬', gaps=True)))
    
    kwlist = groupedkw.groupby(level='theme').nlargest(10).reset_index(level=0, drop=True).to_frame()
    kwlist.reset_index(level=1, inplace=True)
    kwlist.rename(columns={"level_1": "topconcepts"}, inplace=True)
    kwlist_merged = kwlist.groupby('theme')['topconcepts'].apply(list).to_frame()
    kwlist_merged = kwlist_merged.topconcepts.apply(str).to_frame()
    
    grouped = pd.concat([grouped, kwlist_merged], axis=1, sort=True)
    
    grouped.sort_values(by='count', ascending=True, inplace=True)
    
    themes_df = themes_df.rename_axis('thcode').reset_index()
    themes_df.set_index('THlabel', inplace=True)
    
    grouped = grouped.join(themes_df)
    
    source = ColumnDataSource(grouped)
    
    countries = source.data['theme'].tolist()
    
    
    p = figure(plot_width=800, plot_height=400, y_range = countries,
                tools="tap,pan,wheel_zoom,box_zoom,save,reset")
    
    p.hbar(name="myHM", y='theme', right='count', left=0, source=source, height=0.50, color='#4292c6')
    
    title = "Figure 1. Themes addressed by policies, \"" + parea + "\" policy area"
    p.title.text = title
    p.yaxis.axis_label = 'Policy theme'
    #p.xaxis.axis_label = 'Number of initiatives reported'
    
    p.add_layout(LinearAxis(axis_label='Number of policy initiatives reported'), 'above')
    p.title.align = 'right'
    p.title.vertical_align = 'top'
    p.title.text_font_size = '11pt'
    
    p.xaxis.axis_label_text_font_size = "11pt"
    p.xaxis.axis_label_text_font_style="normal"
    p.xaxis.major_label_text_font_size = "10pt"
    
    p.yaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_style="normal"
    p.yaxis.major_label_text_font_size = "10pt"
    
    hover = HoverTool()
    hover.tooltips = """
    <font color="#3eade0">Initiatives:</font> @count <br>
    <font color="#3eade0">Frequent keywords:</font> @topconcepts <br>
    <span style="font-weight: bold;">Click to browse initiatives in STIP Compass</span>
    """
    
    hover.mode = 'hline'
    p.add_tools(hover)

    #Prevent selection on click action to be highlighted
    renderer = p.select(name="myHM")
    renderer.nonselection_glyph = HBar(height=0.50, fill_color='#4292c6', line_color='#4292c6')

    compass= "https://stip.oecd.org/stip/themes/@thcode"
    
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=compass)
    
    save(p)
    


def Fig2(parea, themes):

    writeTo = "templates/figures/" + parea + "/Figure2.html"
    
    output_file(writeTo, mode="inline")
    #NOTE: mode attribute to run output from a local file. In theory, it can be removed for an online file...
    
    #load online stip compass data using pipe '|' separator and skipping the second header (multi-indexing causes problems in the filtering)
    #url = 'https://stip.oecd.org/assets/downloads/STIP_Survey.csv'
    url = 'INPUT/STIP-Data-Flatcsv-Apr2020.csv'
    
    head_df = pd.read_csv(url, sep='|', nrows=1)
    themes_df = head_df[themes]
    themes_df = themes_df.T
    #themes_df.rename(columns={"0": "THlabel"}, inplace=True)
    
    tg_col = [col for col in head_df if col.startswith('TG')]
    targets_df = head_df[tg_col]
    targets_df = targets_df.T
    targets_df.rename(columns={0: "TGlabel"}, inplace=True)
    
    compass_df = pd.read_csv(url, sep='|', skiprows=[1])
    d = ['EGY', 'IDN', 'IND', 'MAR', 'MYS', 'SAU', 'SGL', 'SRB', 'URY', 'VNM']
    compass_df = compass_df[~compass_df['CountryCode'].isin(d)]
    compass_df.drop_duplicates(subset = "InitiativeID", inplace=True)
    compass_df.Tags.fillna("¬", inplace=True)

    compass_df['theme'] = ""
    Fig2_df = pd.DataFrame(columns = compass_df.columns)
    
    for th in themes:
        compass_df.loc[compass_df[th] == "1", th] = 1
        compass_df.loc[compass_df[th] == 1, 'theme'] = themes_df.loc[th].values[0]
        Fig2_df = pd.concat([Fig2_df, compass_df[compass_df[th] == 1]])
    
    Fig2_df.drop_duplicates(subset = "InitiativeID", inplace=True)    
    Fig2_df['count'] = 1

    Fig2_df['target'] = ""
    Fig2b_df = pd.DataFrame(columns = Fig2_df.columns)
    
    for tg in tg_col:
        Fig2_df.loc[Fig2_df[tg] == "1", tg] = 1
        Fig2_df.loc[Fig2_df[tg] == 1, 'target'] = targets_df.loc[tg].values[0]
        Fig2b_df = pd.concat([Fig2b_df, Fig2_df[Fig2_df[tg] == 1]])
    
    grouped = Fig2b_df.groupby('target')[['count', 'HasBeenEvaluated']].sum()
    
    groupedkw = Fig2b_df.groupby('target')['Tags'].apply(lambda x: nltk.FreqDist(nltk.tokenize.regexp_tokenize('¬'.join(x), pattern='¬', gaps=True)))
    
    kwlist = groupedkw.groupby(level='target').nlargest(10).reset_index(level=0, drop=True).to_frame()
    kwlist.reset_index(level=1, inplace=True)
    kwlist.rename(columns={"level_1": "topconcepts"}, inplace=True)
    kwlist_merged = kwlist.groupby('target')['topconcepts'].apply(list).to_frame()
    kwlist_merged = kwlist_merged.topconcepts.apply(str).to_frame()
    
    grouped = pd.concat([grouped, kwlist_merged], axis=1, sort=True)
    
    grouped.sort_values(by='count', ascending=True, inplace=True)
    
    targets_df = targets_df.rename_axis('tgcode').reset_index()
    targets_df.set_index('TGlabel', inplace=True)
    
    grouped = grouped.join(targets_df)
    
    if parea == "Governance":
        alink = "TH1"
    elif parea == "Public research system":
        alink = "TH2"
    elif parea == "Innovation in firms and innovative entrepreneurship":
        alink = "TH3"
    elif parea == "Science-industry knowledge transfer and sharing":
        alink = "TH5"
    elif parea == "Human resources for research and innovation":
        alink = "TH7"
    elif parea == "Research and innovation for society":
        alink = "TH8"
    else: 
        alink = "TH84"
    
    grouped['links'] = "https://stip.oecd.org/ws/STIP/API/getPolicyInitiatives.xqy?format=csv&tg=" + grouped['tgcode'].map(str) + "&th=" + str(alink) + "&br-extra=none,BR16,BR1&br=BR9,BR15"
    
    source = ColumnDataSource(grouped)
    
    targets = source.data['target'].tolist()
    
    
    p = figure(plot_width=800, plot_height=800, y_range = targets,
                tools="tap,pan,wheel_zoom,box_zoom,save,reset")
    
    #p.xaxis.major_label_orientation = pi/4
    
    p.hbar(name="myHM", y='target', right='count', left=0, source=source, height=0.50, color='#4292c6')
    
    title = "Figure 2. Target groups addressed by policies, \"" + parea + "\" policy area"
    p.title.text = title
    p.yaxis.axis_label = 'Target group'
    #p.xaxis.axis_label = 'Number of policy initiatives reported'
    p.add_layout(LinearAxis(axis_label='Number of policy initiatives reported'), 'above')
    p.title.align = 'right'
    p.title.vertical_align = 'top'
    p.title.text_font_size = '11pt'
    
    p.xaxis.axis_label_text_font_size = "11pt"
    p.xaxis.axis_label_text_font_style="normal"
    p.xaxis.major_label_text_font_size = "10pt"
    
    p.yaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_style="normal"
    p.yaxis.major_label_text_font_size = "10pt"
    
    hover = HoverTool()
    hover.tooltips = """
    <font color="#3eade0">Initiatives:</font> @count <br>
    <font color="#3eade0">Frequent keywords:</font> @topconcepts <br>
    <span style="font-weight: bold;">Click to download data</span>
    """
    
    hover.mode = 'hline'
    p.add_tools(hover)
    
    #Prevent selection on click action to be highlighted
    renderer = p.select(name="myHM")
    renderer.nonselection_glyph = HBar(height=0.50, fill_color='#4292c6', line_color='#4292c6')
    
    callback = CustomJS(args={'source': source, 'title': p.title}, code = """
        var idx = source.selected.indices
        var url = source.data['links'][idx]            
        var temptext = title.text
        var tempcolor = title.text_color
        title.text = "Download in progress- this may take up to one minute."
        title.text_color = "red"
        fetch(url, {
              method: 'GET',
            }).then(function(resp) {
              return resp.blob();
            }).then(function(blob) {
              const newBlob = new Blob([blob], { type: "text/csv", charset: "UTF-8" })
        
              // IE doesn't allow using a blob object directly as link href
              // instead it is necessary to use msSaveOrOpenBlob
              if (window.navigator && window.navigator.msSaveOrOpenBlob) {
                window.navigator.msSaveOrOpenBlob(newBlob);
                return;
              }
              const data = window.URL.createObjectURL(newBlob);
              const link = document.createElement('a');
              link.dataType = "json";
              link.href = data;
              link.download = "STIP_COMPASS_Policy_Initiatives_Export.csv";
              link.dispatchEvent(new MouseEvent('click'));
              setTimeout(function () {
                // For Firefox it is necessary to delay revoking the ObjectURL
                window.URL.revokeObjectURL(data), 60
              });
            });
        
        setTimeout(function (){
    
            title.text = temptext
            title.text_color = tempcolor
    
        }, 7000)
    """)
              
    #Add click action
    p.js_on_event(Tap, callback)
    
    save(p)
    
def Fig3(parea, themes):

    writeTo = "templates/figures/" + parea + "/Figure3.html"
    
    output_file(writeTo, mode="inline")
    #NOTE: mode attribute to run output from a local file. In theory, it can be removed for an online file...
    
    #load online stip compass data using pipe '|' separator and skipping the second header (multi-indexing causes problems in the filtering)
    #url = 'https://stip.oecd.org/assets/downloads/STIP_Survey.csv'
    url = 'INPUT/STIP-Data-Flatcsv-Apr2020.csv'
    
    head_df = pd.read_csv(url, sep='|', nrows=1)
    themes_df = head_df[themes]
    themes_df = themes_df.T
    #themes_df.rename(columns={"0": "THlabel"}, inplace=True)
    
    compass_df = pd.read_csv(url, sep='|', skiprows=[1])
    d = ['EGY', 'IDN', 'IND', 'MAR', 'MYS', 'SAU', 'SGL', 'SRB', 'URY', 'VNM']
    compass_df = compass_df[~compass_df['CountryCode'].isin(d)]
    compass_df.Tags.fillna("¬", inplace=True)

    compass_df['theme'] = ""
    Fig3_df = pd.DataFrame(columns = compass_df.columns)
    
    for th in themes:
        compass_df.loc[compass_df[th] == "1", th] = 1
        compass_df.loc[compass_df[th] == 1, 'theme'] = themes_df.loc[th].values[0]
        Fig3_df = pd.concat([Fig3_df, compass_df[compass_df[th] == 1]])
    
    Fig3_df.drop_duplicates(subset = ['InitiativeID', 'InstrumentTypeLabel'], inplace=True)    
    Fig3_df['count'] = 1
    
    grouped = Fig3_df.groupby('InstrumentTypeLabel')[['count', 'HasBeenEvaluated']].sum()
    
    groupedkw = Fig3_df.groupby('InstrumentTypeLabel')['Tags'].apply(lambda x: nltk.FreqDist(nltk.tokenize.regexp_tokenize('¬'.join(x), pattern='¬', gaps=True)))
    
    kwlist = groupedkw.groupby(level='InstrumentTypeLabel').nlargest(10).reset_index(level=0, drop=True).to_frame()
    kwlist.reset_index(level=1, inplace=True)
    kwlist.rename(columns={"level_1": "topconcepts"}, inplace=True)
    kwlist_merged = kwlist.groupby('InstrumentTypeLabel')['topconcepts'].apply(list).to_frame()
    kwlist_merged = kwlist_merged.topconcepts.apply(str).to_frame()
    
    grouped = pd.concat([grouped, kwlist_merged], axis=1, sort=True)
    
    grouped.sort_values(by='count', ascending=True, inplace=True)
    
    inst_index=['Centres of excellence grants', 'Corporate tax relief for R&D and innovation', 'Creation or reform of governance structure or public body', 'Debt guarantees and risk sharing schemes', 'Dedicated support to research infrastructures', 'Emerging technology regulation', 'Equity financing', 'Fellowships and postgraduate loans and scholarships','Formal consultation of stakeholders or experts','Grants for business R&D and innovation','Horizontal STI coordination bodies','Information services and access to datasets','Innovation vouchers','Institutional funding for public research','Intellectual property regulation and incentives','Labour mobility regulation and incentives','Loans and credits for innovation in firms','National strategies, agendas and plans','Networking and collaborative platforms','Policy intelligence (e.g. evaluations, benchmarking and forecasts)','Procurement programmes for R&D and innovation','Project grants for public research','Public awareness campaigns and other outreach activities','Regulatory oversight and ethical advice bodies', 'Science and innovation challenges, prizes and awards', 'Standards and certification for technology development and adoption', 'Technology extension and business advisory services']
    inst_stip={'inst_links': ['Centres_of_excellence_grants', 'Tax_relief', 'Creation_or_reform_of_governance_structure_or_public_body', 'Debt_guarantees_and_risk_sharing_schemes', 'Dedicated_support_to_new_research_infrastructures', 'Emerging_technology_regulation', 'Equity_financing', 'Postgraduate_loans_scholarships_and_fellowships', 'Public_consultation_of_stakeholders', 'Project_grants_for_business_RD_and_innovation', 'Horizontal_STI_coordination_bodies', 'Information_services_and_databases', 'Innovation_vouchers', 'Institutional_funding_for_public_research', 'Intellectual_property_regulation_and_incentives', 'Labour_mobility_regulation_and_incentives', 'Loans_and_credits_for_innovation_in_firms', 'National_strategies_agendas_and_plans', 'Networking_and_collaborative_platforms', 'Policy_intelligence', 'Procurement_programmes_for_RD_and_innovation', 'Project_grants_for_public_research', 'Public_awareness_campaigns_and_other_outreach_activities', 'Regulatory_oversight_and_ethical_advice_bodies', 'Innovation_challenges_prizes_and_awards', 'Standards_and_certification_for_technology_development_and_adoption', 'Technology_transfer_and_business_advisory_services']}
    inst_links_df = pd.DataFrame(data=inst_stip, index=inst_index)
    
    grouped = grouped.join(inst_links_df)
    
    if parea == "Governance":
        alink = "TH1"
    elif parea == "Public research system":
        alink = "TH2"
    elif parea == "Innovation in firms and innovative entrepreneurship":
        alink = "TH3"
    elif parea == "Science-industry knowledge transfer and sharing":
        alink = "TH5"
    elif parea == "Human resources for research and innovation":
        alink = "TH7"
    elif parea == "Research and innovation for society":
        alink = "TH8"
    else: 
        alink = "TH84"
    
    grouped['links'] = "https://stip.oecd.org/ws/STIP/API/getPolicyInitiatives.xqy?format=csv&pi=" + grouped['inst_links'].map(str) + "&th=" + str(alink) + "&br-extra=none,BR16,BR1&br=BR9,BR15"
    
    source = ColumnDataSource(grouped)
    
    instruments = source.data['InstrumentTypeLabel'].tolist()
    
    
    p = figure(plot_width=800, plot_height=800, y_range = instruments,
                tools="tap,pan,wheel_zoom,box_zoom,save,reset")
    
    #p.xaxis.major_label_orientation = pi/4
    
    p.hbar(name="myHM", y='InstrumentTypeLabel', right='count', left=0, source=source, height=0.50, color='#4292c6')
    
    title = "Figure 3. Types of instruments reported, \"" + parea + "\" policy area"
    p.title.text = title
    p.yaxis.axis_label = 'Type of policy instrument'
    #p.xaxis.axis_label = 'Number of instances reported'
    p.add_layout(LinearAxis(axis_label='Number of instances reported'), 'above')
    p.title.align = 'right'
    p.title.vertical_align = 'top'
    p.title.text_font_size = '11pt'
    
    p.xaxis.axis_label_text_font_size = "11pt"
    p.xaxis.axis_label_text_font_style="normal"
    p.xaxis.major_label_text_font_size = "10pt"
    
    p.yaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_style="normal"
    p.yaxis.major_label_text_font_size = "10pt"
    
    hover = HoverTool()
    hover.tooltips = """
    <font color="#3eade0">Instruments:</font> @count <br>
    <font color="#3eade0">Frequent keywords:</font> @topconcepts <br>
    <span style="font-weight: bold;">Click to download data</span>
    """
    
    hover.mode = 'hline'
    p.add_tools(hover)
    
    #Prevent selection on click action to be highlighted
    renderer = p.select(name="myHM")
    renderer.nonselection_glyph = HBar(height=0.50, fill_color='#4292c6', line_color='#4292c6')
    
    callback = CustomJS(args={'source': source, 'title': p.title}, code = """
        var idx = source.selected.indices
        var url = source.data['links'][idx]            
        var temptext = title.text
        var tempcolor = title.text_color
        title.text = "Download in progress- this may take up to one minute."
        title.text_color = "red"
        fetch(url, {
              method: 'GET',
            }).then(function(resp) {
              return resp.blob();
            }).then(function(blob) {
              const newBlob = new Blob([blob], { type: "text/csv", charset: "UTF-8" })
        
              // IE doesn't allow using a blob object directly as link href
              // instead it is necessary to use msSaveOrOpenBlob
              if (window.navigator && window.navigator.msSaveOrOpenBlob) {
                window.navigator.msSaveOrOpenBlob(newBlob);
                return;
              }
              const data = window.URL.createObjectURL(newBlob);
              const link = document.createElement('a');
              link.dataType = "json";
              link.href = data;
              link.download = "STIP_COMPASS_Policy_Initiatives_Export.csv";
              link.dispatchEvent(new MouseEvent('click'));
              setTimeout(function () {
                // For Firefox it is necessary to delay revoking the ObjectURL
                window.URL.revokeObjectURL(data), 60
              });
            });
        
        setTimeout(function (){
    
            title.text = temptext
            title.text_color = tempcolor
    
        }, 7000)
    """)
              
    #Add click action
    p.js_on_event(Tap, callback)
    
    save(p)
    
def Fig4(parea, themes):

    writeTo = "templates/figures/" + parea + "/Figure4.html"
    
    output_file(writeTo, mode="inline")
    #NOTE: mode attribute to run output from a local file. In theory, it can be removed for an online file...
    
    #load online stip compass data using pipe '|' separator and skipping the second header (multi-indexing causes problems in the filtering)
    #url = 'https://stip.oecd.org/assets/downloads/STIP_Survey.csv'
    url = 'INPUT/STIP-Data-Flatcsv-Apr2020.csv'
    
    head_df = pd.read_csv(url, sep='|', nrows=1)
    themes_df = head_df[themes]
    themes_df = themes_df.T
    #themes_df.rename(columns={"0": "THlabel"}, inplace=True)
    
    compass_df = pd.read_csv(url, sep='|', skiprows=[1])
    d = ['EGY', 'IDN', 'IND', 'MAR', 'MYS', 'SAU', 'SGL', 'SRB', 'URY', 'VNM']
    compass_df = compass_df[~compass_df['CountryCode'].isin(d)]
    compass_df.Tags.fillna("¬", inplace=True)

    compass_df['theme'] = ""
    Fig4_df = pd.DataFrame(columns = compass_df.columns)
    
    for th in themes:
        compass_df.loc[compass_df[th] == "1", th] = 1
        compass_df.loc[compass_df[th] == 1, 'theme'] = themes_df.loc[th].values[0]
        Fig4_df = pd.concat([Fig4_df, compass_df[compass_df[th] == 1]])
    
    Fig4_df.drop_duplicates(subset = ['InitiativeID', 'YearlyBudgetRange'], inplace=True)    
    Fig4_df['count'] = 1
    
    grouped = Fig4_df.groupby('YearlyBudgetRange')[['count', 'HasBeenEvaluated']].sum()
    
    groupedkw = Fig4_df.groupby('YearlyBudgetRange')['Tags'].apply(lambda x: nltk.FreqDist(nltk.tokenize.regexp_tokenize('¬'.join(x), pattern='¬', gaps=True)))
    
    kwlist = groupedkw.groupby(level='YearlyBudgetRange').nlargest(10).reset_index(level=0, drop=True).to_frame()
    kwlist.reset_index(level=1, inplace=True)
    kwlist.rename(columns={"level_1": "topconcepts"}, inplace=True)
    kwlist_merged = kwlist.groupby('YearlyBudgetRange')['topconcepts'].apply(list).to_frame()
    kwlist_merged = kwlist_merged.topconcepts.apply(str).to_frame()
    
    grouped = pd.concat([grouped, kwlist_merged], axis=1, sort=True)
    
    grouped.sort_values(by='count', ascending=True, inplace=True)
    
    budgets_index = ['More than 500M', '100M-500M', '50M-100M', '20M-50M', '5M-20M', '1M-5M', 'Less than 1M', 'Not applicable', "Don't know"]
    budgets_stip = {'budgets_links': ['BR15', 'BR14', 'BR13', 'BR12', 'BR11', 'BR10', 'BR9', 'BR16', 'BR1']}
    budgets_links_df = pd.DataFrame(data=budgets_stip, index=budgets_index)
    
    grouped = grouped.join(budgets_links_df)
    
    if parea == "Governance":
        alink = "TH1"
    elif parea == "Public research system":
        alink = "TH2"
    elif parea == "Innovation in firms and innovative entrepreneurship":
        alink = "TH3"
    elif parea == "Science-industry knowledge transfer and sharing":
        alink = "TH5"
    elif parea == "Human resources for research and innovation":
        alink = "TH7"
    elif parea == "Research and innovation for society":
        alink = "TH8"
    else: 
        alink = "TH84"
    
    grouped['links'] = "https://stip.oecd.org/ws/STIP/API/getPolicyInitiatives.xqy?format=csv&th=" + str(alink) + "&br-extra=" + grouped['budgets_links'].map(str)
    
    source = ColumnDataSource(grouped)
    
    budgets = source.data['YearlyBudgetRange'].tolist()
    
    
    p = figure(plot_width=800, plot_height=400, y_range = budgets,
                tools="tap,pan,wheel_zoom,box_zoom,save,reset")
    
    #p.xaxis.major_label_orientation = pi/4
    
    p.hbar(name="myHM", y='YearlyBudgetRange', right='count', left=0, source=source, height=0.50, color='#4292c6')
    
    title = "Figure 4. Policies reported by budget range, \"" + parea + "\" policy area"
    p.title.text = title
    p.yaxis.axis_label = 'Budget range (in EUR)'
    #p.xaxis.axis_label = 'Number of policy initiatives reported'
    p.add_layout(LinearAxis(axis_label='Number of policy initiatives reported'), 'above')
    p.title.align = 'right'
    p.title.vertical_align = 'top'
    p.title.text_font_size = '11pt'
    
    p.xaxis.axis_label_text_font_size = "11pt"
    p.xaxis.axis_label_text_font_style="normal"
    p.xaxis.major_label_text_font_size = "10pt"
    
    p.yaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_style="normal"
    p.yaxis.major_label_text_font_size = "10pt"
    
    hover = HoverTool()
    hover.tooltips = """
    <font color="#3eade0">Initiatives:</font> @count <br>
    <font color="#3eade0">Frequent keywords:</font> @topconcepts <br>
    <span style="font-weight: bold;">Click to download data</span>
    """
    
    hover.mode = 'hline'
    p.add_tools(hover)
    
    #Prevent selection on click action to be highlighted
    renderer = p.select(name="myHM")
    renderer.nonselection_glyph = HBar(height=0.50, fill_color='#4292c6', line_color='#4292c6')
    
    callback = CustomJS(args={'source': source, 'title': p.title}, code = """
        var idx = source.selected.indices
        var url = source.data['links'][idx]            
        var temptext = title.text
        var tempcolor = title.text_color
        title.text = "Download in progress- this may take up to one minute."
        title.text_color = "red"
        fetch(url, {
              method: 'GET',
            }).then(function(resp) {
              return resp.blob();
            }).then(function(blob) {
              const newBlob = new Blob([blob], { type: "text/csv", charset: "UTF-8" })
        
              // IE doesn't allow using a blob object directly as link href
              // instead it is necessary to use msSaveOrOpenBlob
              if (window.navigator && window.navigator.msSaveOrOpenBlob) {
                window.navigator.msSaveOrOpenBlob(newBlob);
                return;
              }
              const data = window.URL.createObjectURL(newBlob);
              const link = document.createElement('a');
              link.dataType = "json";
              link.href = data;
              link.download = "STIP_COMPASS_Policy_Initiatives_Export.csv";
              link.dispatchEvent(new MouseEvent('click'));
              setTimeout(function () {
                // For Firefox it is necessary to delay revoking the ObjectURL
                window.URL.revokeObjectURL(data), 60
              });
            });
        
        setTimeout(function (){
    
            title.text = temptext
            title.text_color = tempcolor
    
        }, 7000)
    """)
              
    #Add click action
    p.js_on_event(Tap, callback)
    
    save(p)
    
    
def Fig5(parea, themes):

    writeTo = "templates/figures/" + parea + "/Figure5.html"
    
    output_file(writeTo, mode="inline")
    #NOTE: mode attribute to run output from a local file. In theory, it can be removed for an online file...
    
    #load online stip compass data using pipe '|' separator and skipping the second header (multi-indexing causes problems in the filtering)
    #url = 'https://stip.oecd.org/assets/downloads/STIP_Survey.csv'
    url = 'INPUT/STIP-Data-Flatcsv-Apr2020.csv'
    
    compass_df = pd.read_csv(url, sep='|', skiprows=[1])
    d = ['EGY', 'IDN', 'IND', 'MAR', 'MYS', 'SAU', 'SGL', 'SRB', 'URY', 'VNM']
    compass_df = compass_df[~compass_df['CountryCode'].isin(d)]
    compass_df.Tags.fillna("¬", inplace=True)
    

    Fig5_df = pd.DataFrame(columns = compass_df.columns)
    
    for th in themes:
        compass_df.loc[compass_df[th] == "1", th] = 1
        Fig5_df = pd.concat([Fig5_df, compass_df[compass_df[th] == 1]])
    
    Fig5_df.drop_duplicates(subset = "InitiativeID", inplace=True)
    Fig5_df['count'] = 1
    
    grouped = Fig5_df.groupby('CoutryLabel')[['count', 'HasBeenEvaluated']].sum()
    
    groupedkw = Fig5_df.groupby('CoutryLabel')['Tags'].apply(lambda x: nltk.FreqDist(nltk.tokenize.regexp_tokenize('¬'.join(x), pattern='¬', gaps=True)))
    
    kwlist = groupedkw.groupby(level='CoutryLabel').nlargest(10).reset_index(level=0, drop=True).to_frame()
    kwlist.reset_index(level=1, inplace=True)
    kwlist.rename(columns={"level_1": "topconcepts"}, inplace=True)
    kwlist_merged = kwlist.groupby('CoutryLabel')['topconcepts'].apply(list).to_frame()
    kwlist_merged = kwlist_merged.topconcepts.apply(str).to_frame()
    
    grouped = pd.concat([grouped, kwlist_merged], axis=1, sort=True)
    
    ccodes_df = pd.read_csv('INPUT/ccodes.csv', index_col='CoutryLabel')
    grouped = grouped.join(ccodes_df)
    
    grouped.sort_values(by='count', ascending=True, inplace=True)
    
    source = ColumnDataSource(grouped)
    
    countries = source.data['CoutryLabel'].tolist()
    
    
    p = figure(plot_width=800, plot_height=1200, y_range = countries,
                tools="tap,pan,wheel_zoom,box_zoom,save,reset")
    
    #p.xaxis.major_label_orientation = pi/4
    
    p.hbar(name="myHM", y='CoutryLabel', right='count', left=0, source=source, height=0.50, color='#4292c6')
    
    title = "Figure 5. Policy initiatives reported under the \"" + parea + "\" policy area"
    p.title.text = title
    p.yaxis.axis_label = 'Country or other reporting entity'
    #p.xaxis.axis_label = 'Number of initiatives reported'
    
    p.add_layout(LinearAxis(axis_label='Number of policy initiatives reported'), 'above')
    p.title.align = 'right'
    p.title.vertical_align = 'top'
    p.title.text_font_size = '11pt'
    
    p.xaxis.axis_label_text_font_size = "11pt"
    p.xaxis.axis_label_text_font_style="normal"
    p.xaxis.major_label_text_font_size = "10pt"
    
    p.yaxis.axis_label_text_font_size = "12pt"
    p.yaxis.axis_label_text_font_style="normal"
    p.yaxis.major_label_text_font_size = "10pt"
    
    hover = HoverTool()
    hover.tooltips = """
    <font color="#3eade0">Initiatives:</font> @count <br>
    <font color="#3eade0">Frequent keywords:</font> @topconcepts <br>
    <span style="font-weight: bold;">Click to browse initiatives in STIP Compass</span>
    
    """
    hover.mode = 'hline'
    p.add_tools(hover)
    
    #Prevent selection on click action to be highlighted
    renderer = p.select(name="myHM")
    renderer.nonselection_glyph = HBar(height=0.50, fill_color='#4292c6', line_color='#4292c6')
    
    if parea == "Governance":
        alink = "TH1"
    elif parea == "Public research system":
        alink = "TH2"
    elif parea == "Innovation in firms and innovative entrepreneurship":
        alink = "TH3"
    elif parea == "Science-industry knowledge transfer and sharing":
        alink = "TH5"
    elif parea == "Human resources for research and innovation":
        alink = "TH7"
    elif parea == "Research and innovation for society":
        alink = "TH8"
    else: 
        alink = "TH84"
    
    compass= "https://stip.oecd.org/stip/countries/@ccode" +"/themes/" + alink
    
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=compass)
    
    save(p)
    