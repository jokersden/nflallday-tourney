def get_top_videos(df):
    df["setnorm"] = df.apply(lambda x: x.set_name.lower().replace(" ", "_"), axis=1)
    df["video_url"] = "https://assets.nflallday.com/editions/"
    df.video_url = (
        df.video_url
        + df.setnorm
        + "/"
        + df.video_id
        + "/play_"
        + df.video_id
        + "_"
        + df.setnorm
        + "_capture_AnimationCapture_Video_Square_Grey_1080_1080_Grey.mp4"
    )
    return (
        df.groupby("video_url")
        .sum()
        .reset_index()
        .nlargest(5, "total")["video_url"]
        .values
    )
