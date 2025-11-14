"""
Extended topic definitions for the AI Quiz Generator.
"""

# Main topic categories
TOPICS = [
    "Science", 
    "History", 
    "Literature", 
    "Technology", 
    "Art", 
    "Geography",
    "Mathematics",
    "Psychology",
    "Languages",
    "Business",
    "Music",
    "Sports"
]

# Detailed topic information with descriptions
TOPIC_INFO = {
    "Science": {
        "description": "Explore the systematic study of the natural world through observation and experimentation.",
        "subtopics": ["Physics", "Chemistry", "Biology", "Astronomy", "Environmental Science"]
    },
    "History": {
        "description": "Discover the study of past events, societies, and civilizations throughout human existence.",
        "subtopics": ["Ancient History", "Medieval History", "Modern History", "World Wars", "Cultural History"]
    },
    "Literature": {
        "description": "Examine written works valued for their artistic merit, ideas, and cultural significance.",
        "subtopics": ["Classical Literature", "Poetry", "Drama", "Fiction", "Non-Fiction"]
    },
    "Technology": {
        "description": "Learn about the application of scientific knowledge for practical applications and innovation.",
        "subtopics": ["Computer Science", "Artificial Intelligence", "Information Technology", "Robotics", "Biotechnology"]
    },
    "Art": {
        "description": "Study visual, auditory or performing artifacts that express the creator's imagination or skill.",
        "subtopics": ["Painting", "Sculpture", "Architecture", "Photography", "Contemporary Art"]
    },
    "Geography": {
        "description": "Investigate the physical features of Earth and its atmosphere, and human activity as it relates to these.",
        "subtopics": ["Physical Geography", "Human Geography", "Cartography", "Climate", "Geopolitics"]
    },
    "Mathematics": {
        "description": "Explore the science of numbers, quantity, and space through abstract concepts and patterns.",
        "subtopics": ["Algebra", "Geometry", "Calculus", "Statistics", "Number Theory"]
    },
    "Psychology": {
        "description": "Study the mind and behavior, exploring both conscious and unconscious phenomena.",
        "subtopics": ["Clinical Psychology", "Cognitive Psychology", "Developmental Psychology", "Social Psychology", "Neuropsychology"]
    },
    "Languages": {
        "description": "Investigate the structural and functional aspects of human communication systems.",
        "subtopics": ["Linguistics", "English", "Spanish", "Chinese", "Arabic"]
    },
    "Business": {
        "description": "Examine organizational activities, management, and commerce in the global economy.",
        "subtopics": ["Marketing", "Finance", "Management", "Entrepreneurship", "Economics"]
    },
    "Music": {
        "description": "Explore the art of sound organized through rhythm, melody, harmony, and timbre.",
        "subtopics": ["Classical Music", "Jazz", "Rock", "Electronic Music", "Music Theory"]
    },
    "Sports": {
        "description": "Study competitive physical activities, games, and athletics from around the world.",
        "subtopics": ["Team Sports", "Individual Sports", "Olympic Games", "Sports History", "Sports Science"]
    }
}

# Expanded topic texts with subtopics
TOPIC_TEXTS = {
    "Science": {
        "Physics": """Physics is the natural science that studies matter, its motion and behavior through space and time, and the related entities of energy and force. 
        It includes classical mechanics, thermodynamics, electromagnetism, relativity, quantum mechanics, and nuclear physics. 
        Isaac Newton established classical mechanics with his three laws of motion. Albert Einstein revolutionized physics with his theories of relativity. 
        Quantum mechanics, developed by scientists like Max Planck, Niels Bohr, and Werner Heisenberg, describes phenomena at the atomic and subatomic levels.""",
        
        "Chemistry": """Chemistry is the scientific discipline involved with elements and compounds composed of atoms, molecules and ions: their composition, structure, properties, behavior and the changes they undergo during a reaction with other substances.
        The periodic table, developed by Dmitri Mendeleev, organizes all chemical elements based on atomic number. Chemical reactions involve the breaking and forming of chemical bonds.
        Key areas include organic chemistry (study of carbon compounds), inorganic chemistry, biochemistry, analytical chemistry, and physical chemistry."""
    },
    
    "History": {
        "Ancient History": """Ancient history covers the period from the beginning of recorded human history to the Early Middle Ages. Major civilizations include Mesopotamia, Ancient Egypt, Ancient Greece, and the Roman Empire.
        Mesopotamia, located between the Tigris and Euphrates rivers, was home to the Sumerian, Babylonian, and Assyrian civilizations. The Sumerians invented the first known writing system, cuneiform.
        Ancient Egypt, famous for its pyramids and pharaohs, developed along the Nile River. The Great Pyramid of Giza, built for Pharaoh Khufu, is the only surviving structure of the Seven Wonders of the Ancient World.""",
        
        "Modern History": """Modern history begins with the Renaissance and continues through the present day, encompassing the Age of Exploration, Industrial Revolution, and two World Wars.
        The Renaissance (14th-17th centuries) was a period of cultural, artistic, political, and scientific rebirth that began in Italy and spread throughout Europe.
        The Age of Exploration (15th-17th centuries) saw European powers exploring, conquering, and colonizing much of the world, establishing global trade networks."""
    },
    
    "Literature": {
        "Fiction": """Fiction refers to literature created from the imagination, not presented as fact, though it may be based on a true story or situation. Its central element is a narrative with plot, characters, and setting.
        Novels are longer works of fiction, while short stories are shorter narratives that typically focus on a single event. Genres include science fiction, fantasy, mystery, romance, and literary fiction.
        Notable novelists include Jane Austen, Charles Dickens, F. Scott Fitzgerald, Gabriel García Márquez, and Toni Morrison, each known for unique styles and themes.""",
        
        "Poetry": """Poetry is a form of literature that uses aesthetic and often rhythmic qualities of language to evoke meanings beyond a prose paraphrase. It often employs meter, rhyme, and various forms of wordplay.
        Traditional forms include sonnets (14 lines, various rhyme schemes), haiku (three lines, 5-7-5 syllable pattern), and epic poems (lengthy narratives often about heroic deeds).
        Major poets include William Shakespeare, Emily Dickinson, Walt Whitman, T.S. Eliot, Pablo Neruda, and Sylvia Plath, representing diverse periods, styles, and cultural perspectives."""
    },
    
    "Technology": {
        "Computer Science": """Computer science is the study of computers and computational systems, including both hardware and software. 
        Alan Turing is considered the father of theoretical computer science and artificial intelligence. His concept of the Turing machine laid the groundwork for modern computing.
        Programming languages like Python, Java, C++, and JavaScript allow humans to communicate instructions to computers. Different languages are optimized for different types of tasks.""",
        
        "Artificial Intelligence": """Artificial Intelligence (AI) is the field of computer science dedicated to creating systems capable of performing tasks that typically require human intelligence.
        Machine learning, a subset of AI, enables computers to learn from data without being explicitly programmed. Deep learning uses neural networks with many layers to analyze complex patterns.
        Natural Language Processing (NLP) focuses on the interaction between computers and human language, enabling applications like machine translation, sentiment analysis, and chatbots."""
    },
    
    "Art": {
        "Painting": """Painting is the practice of applying paint, pigment, color or other medium to a solid surface. The medium is commonly applied to the base with a brush, but other implements, such as knives, sponges, and airbrushes, can be used.
        Throughout history, painting styles have evolved from prehistoric cave paintings to Renaissance masterpieces to modern abstract expressions. Key movements include Impressionism, Cubism, Surrealism, and Abstract Expressionism.
        Famous painters include Leonardo da Vinci, Vincent van Gogh, Pablo Picasso, Frida Kahlo, and Georgia O'Keeffe, each contributing unique perspectives and techniques to the art form.""",
        
        "Architecture": """Architecture is the art and science of designing buildings and other physical structures, combining practical utility with aesthetic appeal.
        Architectural styles have evolved across centuries, from ancient Greek and Roman temples to Gothic cathedrals, from Renaissance palaces to modern skyscrapers and sustainable green buildings.
        Influential architects include Antoni Gaudí, Frank Lloyd Wright, Le Corbusier, I.M. Pei, and Zaha Hadid, each known for distinctive approaches to form, function, and environmental context."""
    },
    
    "Geography": {
        "Physical Geography": """Physical geography focuses on the natural features and processes of the Earth, including landforms, water bodies, climate, soil, and vegetation.
        Major components include geomorphology (study of landforms), climatology (study of climate), hydrology (study of water), biogeography (study of species distribution), and pedology (study of soils).
        Earth's diverse physical regions range from polar ice caps to tropical rainforests, from vast oceans to towering mountain ranges, each with unique ecological characteristics and natural resources.""",
        
        "Human Geography": """Human geography examines the interaction between humans and their environment, focusing on how people organize themselves across space and how they understand and use physical landscapes.
        Key areas include cultural geography, economic geography, political geography, urban geography, and population geography, all exploring different aspects of human-environment relationships.
        Contemporary issues in human geography include urbanization, globalization, sustainable development, climate change adaptation, migration patterns, and cultural landscape preservation."""
    },
    
    "Mathematics": {
        "Algebra": """Algebra is a branch of mathematics dealing with symbols and the rules for manipulating these symbols to solve equations and study mathematical structures.
        Elementary algebra introduces the concept of variables representing numbers, formulation of equations, and techniques for solving these equations. Advanced algebra explores more complex structures and operations.
        Key algebraic concepts include equations, inequalities, functions, polynomials, and abstract algebraic structures like groups, rings, and fields, which have applications across science and engineering.""",
        
        "Geometry": """Geometry is the branch of mathematics concerned with the properties and relations of points, lines, surfaces, solids, and higher dimensional analogs.
        Euclidean geometry, based on axioms and postulates defined by Euclid, focuses on flat space, while non-Euclidean geometries explore curved spaces where parallel lines can intersect or never meet.
        Applications of geometry include computer graphics, architecture, engineering, physics, and astronomy, where spatial relationships and measurements are essential."""
    },
    
    "Psychology": {
        "Cognitive Psychology": """Cognitive psychology is the scientific study of mental processes such as attention, language use, memory, perception, problem solving, creativity, and thinking.
        Key areas include memory (how information is encoded, stored, and retrieved), attention (how we focus on specific stimuli), perception (how we interpret sensory information), and decision-making (how we evaluate options and choices).
        Influential cognitive psychologists include Jean Piaget (cognitive development), Daniel Kahneman (judgment and decision-making), and Elizabeth Loftus (memory distortion), whose work has shaped our understanding of human thought processes.""",
        
        "Social Psychology": """Social psychology examines how people's thoughts, feelings, and behaviors are influenced by the actual, imagined, or implied presence of others.
        Major topics include social influence (conformity, compliance, obedience), social cognition (how we perceive others), attitudes and persuasion, group dynamics, prejudice and discrimination, and prosocial behavior.
        Classic studies include Milgram's obedience experiments, Asch's conformity studies, and Zimbardo's Stanford Prison Experiment, all demonstrating the powerful effects of social situations on individual behavior."""
    },
    
    "Languages": {
        "Linguistics": """Linguistics is the scientific study of language, including its structure, acquisition, and relationship to culture and cognition.
        Major branches include phonetics (speech sounds), phonology (sound systems), morphology (word formation), syntax (sentence structure), semantics (meaning), and pragmatics (language in context).
        Language evolution, acquisition, and diversity are key areas of research, with approximately 7,000 languages spoken worldwide, each with unique features yet sharing fundamental structural principles.""",
        
        "English": """English is a West Germanic language that originated from Anglo-Frisian dialects brought to Britain in the mid 5th to 7th centuries AD by Anglo-Saxon migrants.
        It has evolved over centuries, influenced by Norse, Norman French, Latin, and many other languages, resulting in a rich vocabulary and complex historical development from Old English to Modern English.
        Today, English is a global lingua franca, with approximately 1.5 billion speakers worldwide, serving as the primary language of international business, science, technology, aviation, and diplomacy."""
    },
    
    "Business": {
        "Marketing": """Marketing encompasses the activities and processes for creating, communicating, delivering, and exchanging offerings that have value for customers, clients, partners, and society at large.
        Key elements include market research, product development, branding, advertising, digital marketing, sales strategies, and customer relationship management, all aimed at understanding and meeting consumer needs.
        Modern marketing integrates traditional approaches with data analytics, social media strategies, content marketing, and personalization, adapting to the evolving digital landscape and changing consumer behaviors.""",
        
        "Finance": """Finance is the study and management of money, investments, and other financial assets, dealing with how individuals, businesses, and organizations raise, allocate, and use monetary resources over time.
        Major areas include personal finance (individual money management), corporate finance (business financial decisions), and public finance (government fiscal policies), all involving risk assessment and value optimization.
        Financial markets, including stock exchanges, bond markets, and commodity markets, facilitate the trading of financial assets and provide mechanisms for capital allocation, price discovery, and risk management."""
    },
    
    "Music": {
        "Classical Music": """Classical music is a broad term that usually refers to formal musical traditions of the Western world, encompassing complex compositions written by trained composers for performance.
        It spans multiple periods including Medieval, Renaissance, Baroque, Classical, Romantic, and Modern, each with distinctive styles, forms, and innovations in harmony, melody, and orchestration.
        Notable composers include Johann Sebastian Bach, Wolfgang Amadeus Mozart, Ludwig van Beethoven, Pyotr Ilyich Tchaikovsky, and Claude Debussy, whose works remain central to the classical repertoire.""",
        
        "Rock": """Rock music is a genre of popular music that originated as "rock and roll" in the United States in the late 1940s and early 1950s, developing into various styles since the mid-1960s.
        Characterized by electric guitars, strong beats, and often youth-oriented lyrics, rock has evolved through numerous subgenres including classic rock, progressive rock, punk rock, heavy metal, and alternative rock.
        Influential rock artists include The Beatles, The Rolling Stones, Led Zeppelin, Queen, Pink Floyd, and Nirvana, each contributing to the genre's evolution and cultural impact across generations."""
    },
    
    "Sports": {
        "Team Sports": """Team sports involve groups of players working together toward a shared objective, typically following codified rules and competing against another team.
        Popular team sports include soccer (football), basketball, baseball, cricket, ice hockey, volleyball, and rugby, each with unique gameplay, scoring systems, and team dynamics.
        Benefits of team sports extend beyond physical fitness to include social skills development, communication, cooperation, leadership, and mental well-being through the collective pursuit of common goals.""",
        
        "Olympic Games": """The Olympic Games are the world's foremost sports competition with more than 200 nations participating in summer and winter events held every four years.
        Founded by Pierre de Coubertin in 1894 and first held in Athens in 1896, the modern Olympics revive the ancient Greek tradition of athletic competition among city-states held at Olympia.
        The games feature various events including track and field, swimming, gymnastics, cycling, and combat sports in the Summer Olympics, and skiing, ice skating, and sledding in the Winter Olympics."""
    }
}

def get_all_topic_data():
    """
    Return a comprehensive dictionary of all topic data including 
    main topics, descriptions, subtopics, and content samples
    """
    # Return a dictionary with all topic information
    return {topic: {
        "description": TOPIC_INFO[topic]["description"],
        "subtopics": TOPIC_INFO[topic]["subtopics"]
    } for topic in TOPICS}

def get_topic_sample(topic):
    """Get a sample of the topic content for preview"""
    if topic in TOPIC_TEXTS:
        # If it's a string, return directly
        if isinstance(TOPIC_TEXTS[topic], str):
            return TOPIC_TEXTS[topic]
        # If it's a dictionary, return the first subtopic's content
        elif isinstance(TOPIC_TEXTS[topic], dict) and TOPIC_TEXTS[topic]:
            first_subtopic = next(iter(TOPIC_TEXTS[topic]))
            return TOPIC_TEXTS[topic][first_subtopic]
    return "No content available for this topic."