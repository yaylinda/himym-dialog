setwd("~/Developer/himym-dialog")

#==========================================================
# Read & clean data
#==========================================================
data = read.csv("data.csv")

data$speaker = data$speaker[which(data$speaker == "LILY")] = "Lily"
data$speaker = data$speaker[which(data$speaker == "MARSHALL")] = "Marshall"
data$speaker = data$speaker[which(data$speaker == "TED")] = "Ted"
data$speaker = data$speaker[which(data$speaker == "BARNEY")] = "Barney"
data$speaker = data$speaker[which(data$speaker == "ROBIN")] = "Robin"

main_characters = c(
  "Lily",
  "Marshall",
  "Ted",
  "Barney",
  "Robin"
)

data = subset(data, data$speaker %in% main_characters)

by_speaker_by_episode = aggregate(
  data$num_words,
  by = list(
    season = data$season,
    episode = data$episode,
    speaker = data$speaker
  ),
  sum
)
