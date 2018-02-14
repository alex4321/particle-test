create table if not exists users
(
	uid serial not null
		constraint users_pkey
			primary key
);

create table if not exists followers
(
	id serial not null
		constraint followers_pkey
			primary key,
	follower integer
		constraint followers_follower_users_uid_fk
			references users
				on update cascade on delete cascade,
	target integer
		constraint followers_target_users_uid_fk
			references users
				on update cascade on delete cascade
);

create table if not exists messages
(
	id serial not null
		constraint messages_pkey
			primary key,
	author_id integer not null
		constraint messages_users_uid_fk
			references users
				on update cascade on delete cascade,
	body text not null,
	unix_timestamp numeric not null,
	reply_to integer
		constraint messages_messages_id_fk
			references messages
				on update cascade on delete cascade
);
