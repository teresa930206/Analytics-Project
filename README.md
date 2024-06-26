# Market Basket Analysis for Product Bundling and Customer Behavior 
## **Introduction**
The project focusing on analyze customer buying patterns and product bundling through **Market Basket** and **unsupervised machine learning models(Apriori Algorithm)**, demonstrated thorough analysis and unique metrics, addressing feedback to improve our predictive models and dashboards. Our feature engineering process transforms raw data into actionable insights, while our dashboards and market basket analysis provide valuable tools for product recommendations and sales strategies. 

For App development, I created the **GUI** by **streamlit**.

## **Feature Engineering**
Feature engineering entails converting raw data into features that are appropriate for machine learning models to comprehend and utilize efficiently. The aim is to improve the performance of machine learning algorithms and integrate them into dashboard development by offering meaningful and pertinent input variables.

In this project, I have developed two tables ***the user_feature_table and order_feature_table*** to extract valuable insights and features.

- ***user_feature_table:***
This table is generated to capture various characteristics of each customer.

| Feature | Description |
|----------|----------|
| user_reorder_rate   | Average reorder rate on orders placed.|
| user_unique_products| Distinct product ordered.  |
| user_total_products | Total products ordered. |
| user_avg_cart_size | Mean products per order = average cart size. |
| user_avg_days_between_order | Average days between previous orders. |
| user_reordered_products_ratio | user product reorder ratio.​ |

- ***order_feature_table:***
This table is created to analyze features related to each order, including the **A** and **B** product categories, sales channel, **B** reorder rate, mean order material net value, **A** reorder rate, and sales channel reorder rate.

| Feature | Description |
|----------|----------|
| B_reorder_rate   | Whether the **B** will be reordered in the next order.​   |
| mean_order_material_net_value   | Average order material net value in each order.​ |
| A_reorder_rate | Whether the **A** will be reordered in the next order.​|
| sales_channel_reorder_rate | Whether the sales channel will be used in the next reorder.​|

## **Target Customer Dashboard**
The dashboard is designed to provide comprehensive insights into customer ordering patterns, product sales trends, and key business metrics. Based on the feedback received from our sponsor, we would be refining our dashboard to emphasize critical areas such as sales season analysis and repeated product purchases. 

- ***Reorder Rate By Customer Group:***
>The purpose of the "Reorder Rate By Customer Group" is to analyze and visualize the frequency at which different customer groups reorder products. This graph helps in understanding the buying behavior and loyalty of various customer segments.
- ***Reorder Rate By Product Category(B):***
>The purpose of the "Reorder Rate By Product Category (B)" is to analyze and visualize the frequency at which different product categories are reordered. This graph provides insights into the demand and popularity of various product categories.
- ***Customer Segmentation: Purchase Behavior:***
>**High Total Purchases** indicate a strong demand for dental products.​
>**Diverse Product Range** suggests a diverse requirement for various dental materials and instruments.​
- ***Relationship Between Average Order Gap and Cart Size By Customer Group:***
>Insights from the data can improve inventory management and marketing strategies. Frequent small orders may need streamlined processes, while infrequent large orders could benefit from targeted promotions and outreach to encourage more frequent purchasing.​

![Sample Graph](graphs/Dashboard1.png)

![Sample Graph](graphs/Dashboard2.png)

## **Recommendation: Market Basket Analysis(Apriori Algorithm)**
We have implemented market basket analysis to develop product recommendations. A simple GUI/app has been created, allowing users to input parameters such as customer group, sales channel, and product category. The app then outputs top recommended products that can be bundled or offered as bulk buy promotions. This tool aims to enhance cross-selling and upselling opportunities.
- ***Function:***
>- Used unsupervised  machine learning model (Apriori with association rule).​
>- Data Filtering: Based on user inputs​.
>- Apriori Algorithm: To identify frequent item sets​.
>- Association Rule Mining: To generate recommendation rules.
>- Once we run the model we get the recommendation.​
>- We see recommendations (consequents) and Pickup % (confidence).​
>- Output: Top 5 product recommendations with pickup percentages

![Sample Graph](graphs/Recomendation.png)

## **Market Strategy Recommendation**
Based on the above recommendation from the market basket analysis, we can propose 3 possible focused marketing campaigns for the selected customer group.
- ***Marketing Strategy to Cross-sell and Up-sell products on Website:***
>- Bundle Recommendation (Cross-sell): Suggest complementary products based on the apriori recommendations. 
>-Product Upgrades (Up-sell): Offer upgrades to premium versions of the products they are purchasing. 
![Sample Graph](graphs/Marketing1.png)

- ***Marketing Strategy for Product Bundling Offers:***
>- Promotions and Discounts: Volume Discounts: Discounts based on the volume of purchase, give incentives for bulk orders.
>- Limited-Time Offers: Promote limited-time discounts on bundled packages to create urgency.
>- Targeted Marketing Campaigns:Email Marketing: Segment email lists to target general dentists in the organization and send tailored content about the bundled packages, highlighting the benefits associated.
![Sample Graph](graphs/Marketing2.png)

- ***Marketing Strategy to Incorporate Referral Program:***
>- Loyalty or Referral Programs: Introduce a referral or loyalty program offering points or discounts on future purchases to repeat customer groups. 
![Sample Graph](graphs/Marketing3.png)

- ***Additional Recommendations to Straumann Group:***
>- Website Optimization (Local and global SEO and landing page): Used Semrush and GTMatrix. Use of more Transactional Keywords, Engage in Local SEO, Create targeted Landing Page for product bundling and cross sell upsell offers.
>- Offline Marketing (Trade Shows, Convections, Magazines): Attend and share marketing materials in dental trade shows, dentists conventions and publish information or advertisement in the top dentistry publications.
![Sample Graph](graphs/Marketing4.png)


