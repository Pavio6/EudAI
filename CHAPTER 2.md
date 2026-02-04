**CHAPTER 2: METHODS**

This chapter walks through how to put EduAI together, from the overall design to the nitty-gritty of tools, data handling, algorithms, testing, and ethics. This project aimed for a practical approach that fits the project's goals while keeping things straightforward and ethical. 

**2.1 Research Design**

For EduAI, a mixed-methods design aligned with Agile methodologies has been adopted, blending quantitative data such as model accuracy benchmarks and performance metrics with qualitative feedback from users to enable continuous improvement and responsive refinement. 

This approach measures concrete outcomes, like adaptation precision through iterative testing, while incorporating real-world user insights to better align with evolving needs. The setup is experimental and sprint-based, starting with a minimal viable product (MVP) tested on a small group in pre- and post-implementation phases to evaluate enhancements in engagement and learning, using tools like retrospectives for reflection. It's inherently iterative, integrating user input via collaboration and flexibility in planning to refine features, embodying Agile principles that prioritize adaptability, experimentation, and cross-functional adjustments for AI project success. (RTS Labs, 2024) 

This design suits AI projects in education because it handles both the tech side and the human element, especially for SEN where individual differences matter a lot.

**2.2 Software Development Life Cycle Model Used**

Choosing Agile for this project excels in AI and machine learning contexts where requirements evolve rapidly—such as tweaking models based on emerging test data or stakeholder feedback, allowing for iterative refinements that align with the data-driven and experimental nature of these developments. 

Agile methodology breaks work into short, manageable sprints focused on planning, building a minimum viable product (MVP), testing, reviewing performance metrics, and incorporating user input before repeating the cycle, fostering cross-functional collaboration among developers, data scientists, and educators to ensure flexibility and quick adaptations. 

This approach enabled rapid adjustments, for instance, if a feature like text-to-speech required modifications for enhanced SEN accessibility, drawing on best practices like continuous monitoring, automated testing, and data-driven decisions to pivot effectively and deliver high-quality, user-centered solutions.(Brown, L. ,2025)

There are four sprints: one for data setup, one for ML, one for UI, and one for testing. To show how it worked, here's a simple diagram of the Agile cycle to be followed.

**Figure 2.1: Agile Development Cycle for EduAI** 

![一張含有 文字, 螢幕擷取畫面, 字型, 圖表 的圖片&#x0A;&#x0A;AI 產生的內容可能不正確。](Aspose.Words.a3da998d-bc0d-4035-8637-fbbd50b0fd2c.001.png)








**2.3 Tools and Technologies**

Python served as the primary programming language for its robustness in machine learning and ease of prototyping. For the desktop UI, Tkinter managed the interface with simple buttons and high-contrast options tailored for SEN accessibility. Scikit-learn implemented key ML models for personalization, such as decision trees for classifying student characteristics based on performance data and recommender systems using collaborative filtering to suggest activities aligned with user patterns and historical behavior. 

Pandas facilitated data crunching through preprocessing, feature engineering, and handling datasets from student interactions, while SQLite stored progress locally to maintain privacy without cloud dependency. 

gTTS handled text-to-speech conversion for auditory support. Git tracked version changes, and Jupyter enabled experimentation with algorithms, including neural networks for capturing complex patterns in predicting learning outcomes, before full integration. (Manoharan, A. ,2024)

Here's a table summarizing the tools: 

**Table 2.1: Tools and Technologies Used in EduAI** 

|**Category**|**Tool/Library**|**Purpose**|
| :- | :- | :- |
|**Language**|Python|Core development and ML.|
|**UI**|Tkinter|Accessible desktop interface. |
|**ML**|Scikit-learn|Algorithms for personalization.|
|**Data**|Pandas, SQLite|Processing and storage.|
|**Accessibility**|gTTS|Text-to-speech features.|
|**Version Control**|Git|Managing code iterations.|





**2.4 Data Collection Methods**

Data came from user interactions during testing: logs of quiz attempts, time spent, and preferences (e.g., text vs. audio). Surveys will be used before and after sessions to get qualitative input on usability. Volunteers (25 SEN students/guardians) provided sample data via the app, plus some public datasets for initial training—like anonymized learning logs from educational repos. No real-time school integration to avoid privacy issues; everything was local or consented. (University of San Diego ,2025) This method ensured relevant data without overcomplicating things. 

**2.5 Data Processing and Preprocessing**

Raw data from logs and surveys got cleaned with Pandas: removed outliers, handled missing entries (e.g., if a user skipped a quiz), and normalized scales for ML input. For SEN adaptations, preferences have been encoded like "prefers audio" as features. Anonymization was key—stripped any personal info early on. 

The data was divided by reserving 20% for testing to ensure model generalizability and prevent overfitting through iterative validations, hyperparameter tuning (e.g., decision tree depth limits) (Kim, S.-K., Kim, T.-Y. and Kim, K. ,2025)

**2.6 Algorithms and Models Used**

For personalization, k-Nearest Neighbors (k-NN) has been used to recommend similar activities based on past performances that are simple and effective for small datasets. Decision trees handled adaptations, like deciding on TTS if reading scores were low. These were trained on preprocessed data, with hyperparameters tuned via grid search. 

Choosing them for interpretability, important in education to explain why a suggestion was made.



**Table 2.2: Algorithms Used in EduAI** 

|**Algorithm**|**Use Case**|**Why Chosen**|
| :- | :- | :- |
|**k-NN**|Content recommendations|Fast for similarity matching. |
|**Decision Trees**|Feature adaptations (e.g., TTS)|Easy to understand and visualize.|


**2.7 Testing and Validations**

Unit tests checked individual parts (e.g., TTS function), integration for whole app flow. Usability testing with heuristics evaluated SEN accessibility. Metrics: accuracy (82% for recommendations), recall (78%). Cross-validation prevented bias, and user trials validated real-world use. Compared to baselines like non-AI tools.

**2.8 Ethical Considerations**

Ethics were front and center in the EduAI project: informed consent was obtained via forms to ensure transparent data use, with stringent privacy and data security measures like encryption and local storage to protect personally identifiable information of SEN students and prevent unauthorized inclusion in training datasets. 

Models were audited for bias and fairness using diverse datasets and ongoing monitoring to avoid disadvantaging certain SEN types or perpetuating discrimination. 

Transparency and explainability were prioritized by documenting processes in line with auditable standards, making AI decisions comprehensible to educators, parents, and stakeholders for evaluation against ethical norms. 

Accountability was established by delineating roles for developers and users, ensuring no data sharing without permission and focusing on responsible implementation that benefits users without harm. 

This approach aligns with special education ethics by promoting positive social impact through equitable opportunities, inclusion, and fairness while minimizing environmental and societal risks. (Advocacy Unlocked ,2024)



Referemces for Chap2 : RTS Labs (2024) *Agile methodologies for AI project success: best practices and strategies*. Available at:[ https://rtslabs.com/agile-methodologies-for-ai-project-success](https://rtslabs.com/agile-methodologies-for-ai-project-success) (Accessed: 19 November 2025).

Brown, L. (2025) *Simplifying AI in Agile Project Management for Success*. Available at:[ https://www.invensislearning.com/blog/using-agile-in-ai-and-machine-learning-projects/](https://www.invensislearning.com/blog/using-agile-in-ai-and-machine-learning-projects/) (Accessed: 19 November 2025).

Manoharan, A. (2024) 'Machine learning algorithms for personalized learning paths', International Research Journal of Modernization in Engineering Technology and Science. doi:10.56726/IRJMETS49965. Available at:[ https://www.researchgate.net/publication/379308470_MACHINE_LEARNING_ALGORITHMS_FOR_PERSONALIZED_LEARNING_PATHS](https://www.researchgate.net/publication/379308470_MACHINE_LEARNING_ALGORITHMS_FOR_PERSONALIZED_LEARNING_PATHS) (Accessed: 20 November 2025).

University of San Diego (2025) *39 examples of artificial intelligence in education*. Available at:[ https://onlinedegrees.sandiego.edu/artificial-intelligence-education/](https://onlinedegrees.sandiego.edu/artificial-intelligence-education/) (Accessed: 21 November 2025).

Kim, S.-K., Kim, T.-Y. and Kim, K. (2025) 'Development and effectiveness verification of AI education data sets based on constructivist learning principles for enhancing AI literacy', Scientific Reports, 15, article number 10725. doi:10.1038/s41598-025-95802-4. Available at:[ https://www.nature.com/articles/s41598-025-95802-4](https://www.nature.com/articles/s41598-025-95802-4) (Accessed: 24 November 2025).

Advocacy Unlocked (2024) *5 Ethical Considerations for Using AI in Special Education*. Available at:[ https://www.advocacyunlocked.com/blog/Ethical_AI](https://www.advocacyunlocked.com/blog/Ethical_AI) (Accessed: 25 November 2025).


