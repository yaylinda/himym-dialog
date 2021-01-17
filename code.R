setwd("~/Developer/himym-dialog")

library(ggplot2)
library(treemapify)

#==========================================================
# Read & clean data
#==========================================================
data = read.csv("data.csv")

data$speaker[which(data$speaker == "LILY")] = "Lily"
data$speaker[which(data$speaker == "MARSHALL")] = "Marshall"
data$speaker[which(data$speaker == "TED")] = "Ted"
data$speaker[which(data$speaker == "BARNEY")] = "Barney"
data$speaker[which(data$speaker == "ROBIN")] = "Robin"

main_characters = c(
  "Lily",
  "Marshall",
  "Ted",
  "Barney",
  "Robin"
)

data = subset(data, data$speaker %in% main_characters)
temp = subset(data, data$season == 1)
#==========================================================
# Aggregations
#==========================================================

by_speaker_by_episode = aggregate(
  data$num_words,
  by = list(
    season = data$season,
    episode = data$episode,
    speaker = data$speaker
  ),
  sum
)
by_speaker_by_episode$episode_count = 1

num_episodes_per_season = aggregate(
  by_speaker_by_episode$episode,
  by = list(
    season = by_speaker_by_episode$season
  ),
  max
)


#==========================================================
# Plots
#==========================================================

