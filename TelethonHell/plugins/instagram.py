import os
import re
import requests

from . import *


@hell_cmd(pattern="igdl(?:\s|$)([\s\S]*)")
async def download(event):
    flag, url = await get_flag(event)
    _, _, hell_mention = await client_id(event)
    hell = await eor(event, "IG downloader in action...")
    
    if flag.lower() in ["-post", "-story"]:
        result = re.search(insta_regex, url)
        if not result:
            return await parse_error(hell, "No link to download.")
        try:
            file, caption = await IGDL(event, result.group(0))
        except Exception as e:
            return await parse_error(hell, e)

        items_list = os.listdir("./insta/dl")
        count = 0
        if items_list != []:
            for i in items_list:
                file = open(f"./insta/dl/{i}", "rb")
                x = await event.client.send_message(
                    event.chat_id, 
                    file=file, 
                    message=f"📥 InstaGram Post Downloaded By :- {hell_mention}",
                )
                if caption:
                    await event.client.send_message(
                        event.chat_id,
                        message=caption,
                        reply_to=x,
                    )
                os.remove(f"./insta/dl/{i}")
                count += 1
            await eod(hell, f"**Downloaded Instagram Post!** \n\n__Total:__ `{count} posts.`")
        else:
            await parse_error(hell, "Unable to upload video! Check LOGS and try again!")

    elif flag.lower() == "-htag":
        # TODO: No.of posts given by user and not default to 10
        if url and url.startswith("#"):
            await hell.edit(f"IG downloader in action... \n\nUploading top 10 posts of `#{url}`")
            try:
                await IG_Htag_DL(event, url[1:], 10)
                items_list = os.listdir("./insta/dl")
                count = 0
                for i in items_list:
                    file = open(f"./insta/dl/{i}", "rb")
                    await event.client.send_message(
                        event.chat_id, 
                        file=file,
                    )
                    os.remove(f"./insta/dl/{i}")
                    count += 1
                await hell.edit(f"**Downloaded top posts of** `{url}` \n\n__Total:__ `{count} posts.`")
            except Exception as e:
                return await parse_error(hell, e)
        else:
            return await eod(hell, f"**SYNTAX EXAMPLE:** \n\n`{hl}igdl -htag #amvs`\n\nThis will give top 10 IG posts of hashtag `#amvs`.")
    else:
        await eod(hell, f"Give proper flag. Check `{hl}plinfo instagram` for details.")
    

@hell_cmd(pattern="igup(?:\s|$)([\s\S]*)")
async def upload(event):
    flag, url = await get_flag(event)
    hell = await eor(event, "IG uploader in action...")
    reply = await event.get_reply_message()
    caption = f"{reply.message} \n\n" if reply.message else ""
    caption += "• #UploadedByHellBot"
    HELL_MEDIA = media_type(reply)

    try:
        IG = await InstaGram(event)
    except Exception as e:
        return await parse_error(hell, e)

    if not reply:
        return await eod(hell, "Reply to a media to upload on instagram.")
    if not reply.media:
        return await eod(hell, "Reply to a media to upload on instagram.")

    if flag.lower() == "-reel":
        if HELL_MEDIA not in ["Gif", "Video"]:
            return await eod(hell, "A reel can only be GIF or Video!")
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading reel to instagram...")
        try:
            video = IG.clip_upload(path=file, caption=caption)
        except Exception as e:
            os.remove(file)
            return await parse_error(hell, e)
        await hell.edit(f"**Uploaded Reel to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)
    
    elif flag.lower() == "-tv":
        if HELL_MEDIA not in ["Gif", "Video"]:
            return await eod(hell, "An IGTV can only be GIF or Video!")
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading IGTV to instagram...")
        try:
            video = IG.igtv_upload(path=file, title=caption, caption=caption)
        except Exception as e:
            os.remove(file)
            return await parse_error(hell, e)
        await hell.edit(f"**Uploaded IGTV to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)
    
    elif flag.lower() == "-vid":
        if HELL_MEDIA not in ["Gif", "Video"]:
            return await eod(hell, "A video post can only be GIF or Video!")
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading Video to instagram...")
        try:
            video = IG.video_upload(path=file, caption=caption)
        except Exception as e:
            os.remove(file)
            return await parse_error(hell, e)
        await hell.edit(f"**Uploaded Video to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)

    elif flag.lower() == "-pic":
        if HELL_MEDIA != "Photo":
            return await eod(hell, "A picture post can only be a Photo!")
        file = await event.client.download_media(reply)
        await hell.edit("**Downloaded!** \n\nNow uploading Photo to instagram...")
        try:
            video = IG.photo_upload(path=file, caption=caption)
        except Exception as e:
            os.remove(file)
            return await parse_error(hell, e)
        await hell.edit(f"**Uploaded Photo to Instagram!** \n\n[See Post From Here](https://instagram.com/p/{video.code})", link_preview=False)
        os.remove(file)

    elif flag.lower() == "-story":
        if HELL_MEDIA in ["Gif", "Video"]:
            file = await event.client.download_media(reply)
            await hell.edit("**Downloaded!** \n\nNow uploading Story to instagram...")
            try:
                video = IG.video_upload_to_story(path=file, caption=caption)
            except Exception as e:
                os.remove(file)
                return await parse_error(hell, e)
            await hell.edit(f"**Uploaded Story to Instagram!** \n\n[See Story From Here](https://instagram.com/p/{video.code})", link_preview=False)
            os.remove(file)

        elif HELL_MEDIA == "Photo":
            file = await event.client.download_media(reply)
            await hell.edit("**Downloaded!** \n\nNow uploading Story to instagram...")
            try:
                video = IG.photo_upload_to_story(path=file, caption=caption)
            except Exception as e:
                os.remove(file)
                return await parse_error(hell, e)
            await hell.edit(f"**Uploaded Story to Instagram!** \n\n[See Story From Here](https://instagram.com/p/{video.code})", link_preview=False)
            os.remove(file)
        
        else:
            return await parse_error(hell, "Invalid media format. Only Videos, Pictures, GIF are supported to upload story.")

    else:
        await eod(hell, f"Give proper flag. Check `{hl}plinfo instagram` for details.")
    

@hell_cmd(pattern="iguser(?:\s|$)([\s\S]*)")
async def userinfo(event):
    uname = event.text.split(" ", 2)[1]
    username = uname.replace("@", "") if "@" in uname else uname
    hell = await eor(event, f"Searching `{username}` on Instagram...")
    info_str = """
<b><i><u>•×• Instagram User Details •×•</b></i></u>
    
<b>• Username:</b> <code>{}</code>
<b>• Full Name:</b> <code>{}</code>
<b>• Private:</b> <code>{}</code>
<b>• Verified:</b> <code>{}</code>
<b>• Posts:</b> <code>{}</code>
<b>• Followers:</b> <code>{}</code>
<b>• Followings:</b> <code>{}</code>
<b>• Website:</b> <code>{}</code>
<b>• Business:</b> <code>{}</code>
<b>• Email:</b> <code>{}</code>
<b>• Bio:</b> <code>{}</code>

<a href='https://www.instagram.com/{}/'>Link To Profile 🔗</a>
"""
    IG = await InstaGram(event)
    if IG:
        info = IG.user_info_by_username(username).dict()
        username = info['username'] if info['username'] else "No Username"
        full_name = info['full_name'] if info['full_name'] else "No Fullname"
        private = info['is_private']
        profile_pic = info['profile_pic_url_hd'] if info['profile_pic_url_hd'] else info['profile_pic_url']
        verified = info['is_verified']
        posts = info['media_count']
        followers = info['follower_count']
        following = info['following_count']
        bio = info['biography'] if info['biography'] else "No Bio"
        url = info['external_url'] if info['external_url'] else "No Website"
        business = info['is_business']
        email = info['public_email'] if info['public_email'] else "No Email"
        ppic = requests.get(profile_pic)
        open(f"{username}.jpg", "wb").write(ppic.content)
        image = f"{username}.jpg"
        output = info_str.format(
            username,
            full_name,
            private,
            verified,
            posts,
            followers,
            following,
            url,
            business,
            email,
            bio,
            username,
        )
        await event.client.send_message(
            event.chat_id,
            output[:1024], # as 1024 is telegram limit for media captions
            file=image,
            force_document=False,
            parse_mode="HTML",
            link_preview=False,
        )
        await hell.delete()
        os.remove(f"{username}.jpg")
    else:
        await parse_error(hell, "`INSTAGRAM_SESSION` __not configured or Expired !__", False)


CmdHelp("instagram").add_command(
    "igdl", "<flag> <link>", "Download posts/reels/stories from Instagram. Requires INSTAGRAM_SESSION to work."
).add_command(
    "iguser", "<username>", "Extracts the data of given username from Instagram."
).add_command(
    "igup", "<flag> <reply>", "Upload replied media on Instagram with caption from Telegram."
).add_extra(
    "🚩 Flags [igdl]", "-post, -story, -htag"
).add_extra(
    "🚩 Flags [igup]", "-reel, -tv, -vid, -pic, -story"
).add_info(
    "Instagram API for Telegram."
).add_warning(
    "✅ Harmless Module"
).add()