const fs = require('fs')
const config = require("./config.js")

if( !fs.existsSync(`./${config.folder}`) ) fs.mkdirSync(`./${config.folder}`)

const streams = {}

const Discord = require("discord.js")
const client = new Discord.Client()
var recorder= false
var voiceChannel2= false
var connection2=false
var message2=false
client.on('ready', () => {
    console.log("Ready")
})



client.on('message', message => {
    //if( !config.master.includes(message.author.id) ) {
	//	console.log("invalid use")
	//	return}

    //Usage: record channel-name
    if( message.cleanContent.startsWith('w!startrecording') ) {
        var [command, ...channel] = message.cleanContent.split(/\s+/)
		channel = ['Recording']
		console.log(channel)
        var voiceChannel = client.channels.cache.find(c => c.name.toLowerCase() === channel.join(" ").toLowerCase().replace("#","") )
		voiceChannel = message.guild.channels.cache.get('803547586581102595')
		voiceChannel2 =voiceChannel
	
        if( voiceChannel ) {
            //Create new stream writer
            //streams[voiceChannel.id] = fs.createWriteStream(`./${config.folder}/${voiceChannel.name}.pcm`)
            //Join channel
			//streams[voiceChannel.id]=fs.createWriteStream(`./${config.folder}/${voiceChannel.name}.pcm`)
			
            voiceChannel.join().then( connection => {
				console.log('Set channel')
				connection2=connection
				message2 =message
				recorder=true 
				
				
                //console.log("connected")
				//connection.play('./beep.mp3')
                //Create a receiver
                //var receiver = connection.receiver()
                //Route buffer to out stream
               
				//const audio=connection.receiver.createStream(message.author,{ mode: 'pcm' ,end: 'manual'})
				
				//streams[voiceChannel.id]=fs.createWriteStream(`./${config.folder}/${voiceChannel.name}.pcm`)
                //audio.pipe(streams[voiceChannel.id])
				
                //message.reply(`Recording ${voiceChannel.name} ...`)
            })    
        }    
    }

    //Usage: stop channel-name
   // if( message.cleanContent.startsWith('stop') ) {
    //    var [command, ...channel] = message.cleanContent.split(/\s+/)
     //   var voiceChannel = client.channels.cache.find(c => c.name.toLowerCase() === channel.join(" ").toLowerCase().replace("#","") )

     //   if( voiceChannel ) {
            //Try leave voice channel
    //        try { voiceChannel.leave() } catch(e) { console.error(e) }
            //Try close stream
            //try { streams[voiceChannel.id].close() } catch(e) { console.error(e) }
            //Delete stream reference
            //console.log (streams)
	//		streams[voiceChannel.id].end()
	//		delete streams[voiceChannel.id]

    //        message.reply(`Recording on ${voiceChannel} has finished`)
    //    }    
    //}
    
    //Usage: play stuff
//    if( message.cleanContent.startsWith('state') ) {
//		var [command, ...channel] = message.cleanContent.split(/\s+/)
 //       var voiceChannel = client.channels.cache.find(c => c.name.toLowerCase() === channel.join(" ").toLowerCase().replace("#","") )
 //       voiceChannel.join().then(connection => {
//			connection.play('./beep.mp3')//(`./${config.folder}/${voiceChannel.name}.pcm`,{type:'opus'})
			
//			const stream = fs.createReadStream(`./${config.folder}/${voiceChannel.name}.pcm`);
//			const dispatcher = connection.play(stream, {
//				type: "converted"
//			});
			
			
			//const broadcast = client.voice.createBroadcast()
			//broadcast.play(`./${config.folder}/${voiceChannel.name}.pcm`,{type:'opus'})
			//connection.play(broadcast)
			
			
			//voiceChannel.leave()
//		});
 //   }    
})

client.on('voiceStateUpdate', (oldMember, newMember) => {
	if (recorder){
		
		var voiceChannel=voiceChannel2 
		var connection=connection2 
		var message= message2 
		let newUserChannel = newMember.channelID
		let oldUserChannel = oldMember.channelID
		console.log(newUserChannel)
		console.log(voiceChannel.id)
		console.log(client.user.id)

		if(newUserChannel === voiceChannel.id && newMember.member.user.id!==client.user.id) {
			// User Joins a voice channel
			console.log('hallo')
			connection.play('/home/pi/walross_bot/walross.mp3')
			console.log("Joined VC1")
			const audio=connection.receiver.createStream(newMember.member.user,{ mode: 'pcm' ,end: 'manual'})//message.author
			console.log(voiceChannel.id)
			
			streams[voiceChannel.id]=fs.createWriteStream(`./${config.folder}/voice.pcm`)
			audio.pipe(streams[voiceChannel.id])
			//console.log(streams[voiceChannel.id])
			message.reply(`Nimmt gerade eine wichtige Nachricht auf...`)
			

		} else if(oldUserChannel === voiceChannel.id&& oldMember.member.user.id!==client.user.id){
			// User leaves a voice channel
			
			
			try { voiceChannel.leave() } catch(e) { console.error(e) }
			//try { streams[voiceChannel.id].close() } catch(e) { console.error(e) }
			streams[voiceChannel.id].end()
			//console.log(streams[voiceChannel.id])
			delete streams[voiceChannel.id]

			message.reply(`ist fertig`)
			console.log("Left VC1")
			
			recorder=false
			
		}
	}
	 
})

client.login(config.token)

function close (code) {
    client.channels.get(config.channel).leave()
    console.log(`Completed recording`)
    process.exit(0)
}

process.on('SIGINT', close)
process.on('SIGTERM', close)

