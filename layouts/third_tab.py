# layout for the third tab of the dashboard

# built-in modules
import dash_core_components as dcc

# configs
from configs.DashConfigs import selected_tab_style, selected_side_tab_style

# figures
from layouts.third_tab_layouts.facility_needs import get_facility_sentiment_map, get_sentiment_scatterplot, get_clusters_table, get_clusters_scatterplot
from layouts.third_tab_layouts.all_responses import get_all_needs_table, get_all_needs_cluster_scatterplot
from layouts.third_tab_layouts.how_participate import get_how_participate_table, get_how_participate_scatterplot, get_how_participate_bars
from layouts.third_tab_layouts.culture_improvement import get_culture_improvement_table, get_culture_improvement_scatterplot, get_culture_improvement_bars
from layouts.third_tab_layouts.shining_culture import get_shining_culture_table, get_shining_culture_scatterplot
from layouts.third_tab_layouts.culture_definition import get_culture_def_table, get_culture_def_scatterplot
from layouts.third_tab_layouts.missing_goals import get_missing_goals_table, get_missing_goals_scatterplot
from layouts.third_tab_layouts.goal_definitions import get_goal_definitions_table

#############################
# Layout Functions
#############################
def get_tab_layout():
    return dcc.Tab(label = "Results of Analysis",
                   children = [
                              dcc.Tabs(vertical = True,
                                       children = [
                                                dcc.Tab(label = "Status of Facilities",
                                                        children = [get_facility_sentiment_map(), get_sentiment_scatterplot(), get_clusters_table(), get_clusters_scatterplot()],
                                                        selected_style = selected_side_tab_style),
                                                dcc.Tab(label = "Needs of the Community",
                                                        children = [get_all_needs_table(), get_all_needs_cluster_scatterplot()],
                                                        selected_style = selected_side_tab_style),
                                                dcc.Tab(label = "Cultural Participation",
                                                        children = [get_how_participate_table(), get_how_participate_scatterplot()] + get_how_participate_bars(),
                                                        selected_style = selected_side_tab_style),
                                                dcc.Tab(label = "Areas making Good Progress",
                                                        children = [get_shining_culture_table(), get_shining_culture_scatterplot()],
                                                        selected_style = selected_side_tab_style),
                                                dcc.Tab(label = "Areas for Improvement",
                                                        children = [get_culture_improvement_table(), get_culture_improvement_scatterplot()] + get_culture_improvement_bars(),
                                                        selected_style = selected_side_tab_style),
                                                dcc.Tab(label = "Community's Definiton \n of Culture",
                                                        children = [get_culture_def_table(), get_culture_def_scatterplot()],
                                                        selected_style = selected_side_tab_style),
                                                dcc.Tab(label = "Missing Cultural Goals",
                                                        children = [get_missing_goals_table(), get_missing_goals_scatterplot()],
                                                        selected_style = selected_side_tab_style),
                                                dcc.Tab(label = "Community's Needs \n for Existing Goals",
                                                        children = [get_goal_definitions_table()],
                                                        selected_style = selected_side_tab_style)
                                                ], style={'padding-top': 15})

                            ], selected_style = selected_tab_style)

#############################################################
#############################################################
