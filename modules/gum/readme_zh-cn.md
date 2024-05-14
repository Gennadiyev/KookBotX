# kbX `UserManager` 设计

> `gum` 为 Global User Manager 的缩写。

> [!WARNING]
> 本项目所包含的 `JSONUserManager` 为示例实现，供开发者参考。由于写入、读取必须读全文，该方案不适用于大规模数据。欢迎设计更适合自己项目的 `UserManager`（如 `MySQLUserManager`、`SQLiteUserManager` 等）。

## API 说明

### 用户注册：`register`

**参数** 需要 `user_id`（唯一键，必须）和 `game_id`（非必须）来记录是哪个游戏促使用户注册账户。

**行为** 在 `self.data_dir` 下创建随机名字 `s` 的空文件夹表示该用户数据，然后在用户表中注册 `user_id -> s` 的映射关系。最后，在空文件夹下创建 `meta.json` 用来储存用户元信息，创建 `backups` 文件夹用来储存该用户的数据备份。

**报错** 如果用户已经在用户表中，则上报 `DuplicateRegistrationError`。任何其他错误都会被捕捉并原样上报，此时用户表会滚回。

### 反注册：`unregister`

**参数** 需要 `user_id`（唯一键，必须）来反注册用户。

**行为** 在用户表中删除 `user_id`。对应的文件夹不会被删除。

**报错** 如果用户不在用户表中，则上报 `UserNotFoundError`。任何其他错误都会被捕捉并原样上报，此时用户表会滚回。

### 保存用户表：`save_user_table`

**行为** 将用户表保存到 `self.data_dir / 'user_table.json'` 文件中。（取决于实现，也可以不使用 JSON 格式。）

**报错** 任何错误都会被捕捉并原样上报。

### 用户是否存在：`has_user`

**参数** 需要 `user_id` 来查询用户是否存在。

**行为** 检查用户表中是否有 `user_id`。

**报错** 任何错误都会被捕捉并原样上报。

### 查询数据：`get_data_for_game`

**参数** 需要 `user_id` 和 `game_id` 来查询用户在某个游戏的数据。

**行为** 检查用户表中是否有 `user_id`，如果没有则上报 `UserNotFoundError`。如果有则检查对应的文件夹下是否有 `game_id.dat` 的数据文件，如果没有则上报 `GameDataNotFoundError`。如果有则读取数据文件并返回，此过程中任何错误都会上报 `GameDataCorruptionError`。只会返回 `bytes` 类型的数据。

**报错** 如果用户不在用户表中，则上报 `UserNotFoundError`。如果用户在用户表中但没有对应的游戏数据，则上报 `GameDataNotFoundError`。如果数据文件损坏，则上报 `GameDataCorruptionError`。

### 写入数据：`set_data_for_game`

**参数** 需要 `user_id` 和 `game_id` 来写入用户在某个游戏的数据。此外，需要 `data`（类型必须为 `bytes`）来确认所写入的数据。`backup` 开关（可选）表示是否备份原数据。

**行为** 检查用户表中是否有 `user_id`，如果没有则上报 `UserNotFoundError`。然后，如果 `backup=True`，则备份 `game_id.bak`（若有）到对应 `backups` 文件夹下，以 `game_id.dat.{timestamp}.bak` 的名字保存。最后，写入新的 `game_id.dat` 数据。

**报错**

- 如果用户不在用户表中，则上报 `UserNotFoundError`。任何其他错误都会被捕捉并原样上报。
- 如果 `backup=True`，任何在备份时的报错都会上报 `BackupError`，此时 `game_id.dat` 文件不会被写入。
- 如果写入数据时出错，则上报 `GameDataCorruptionError`，此时 `game_id.dat` 文件不会被写入。

### 是否存在数据：`has_data_for_game`

**参数** 需要 `user_id` 和 `game_id` 来查询用户在某个游戏是否有数据。

**行为** 如果 `user_id` 未注册，或者 `game_id.dat` 不存在，则返回 `False`。否则返回 `True`。

### 删除数据：`delete_data_for_game`

**参数** 需要 `user_id` 和 `game_id` 来删除用户在某个游戏的数据。

**行为** 检查用户表中是否有 `user_id`，如果没有则上报 `UserNotFoundError`。然后，将 `game_id.dat` 移动到对应 `backups` 文件夹下，以 `game_id.dat.{timestamp}.del` 的名字保存。

**报错** 如果用户不在用户表中，则上报 `UserNotFoundError`。任何其他错误都会被捕捉，此时 `game_id.dat` 文件不会被删除。

### 获取 `meta` 元数据：`meta_get`

**参数** 需要 `user_id` 来获取用户的元数据。

**行为** 检查用户表中是否有 `user_id`，如果没有则上报 `UserNotFoundError`。然后读取对应文件夹下的 `meta.json` 文件，返回 `dict` 类型的数据。

**报错** 如果用户不在用户表中，则上报 `UserNotFoundError`。读取 `meta.json` 文件时不应出错。任何其他错误都会被捕捉并原样上报。

### 写入 `meta` 元数据：`meta_set`

**参数** 需要 `user_id`（唯一键）和 `meta_key`、`meta_value` 来写入用户的元数据。

**行为** 检查用户表中是否有 `user_id`，如果没有则上报 `UserNotFoundError`。然后读取对应文件夹下的 `meta.json` 文件并备份到 `backups` 文件夹下，以 `meta.json.{timestamp}.bak` 的名字保存。最后写入新的 `meta_key` 和 `meta_value`。

**报错** 如果用户不在用户表中，则上报 `UserNotFoundError`。读取 `meta.json` 文件时不应出错。任何其他错误都会被捕捉并原样上报。

### DEBUG：`dump_user_table`

## 说明与设计法则

- 可以注意到上文对用户的 `meta` 元信息强制了 `json` 格式，而对游戏所写入的数据则没有限制（`bytes` 类型）。
- 在没有开发者干预时，虽然有备份，`UserManager` **不应当** 回滚用户元数据或游戏数据。
- 游戏数据不是加密存储的，`game_id` 也不是加密的。默认情况下，开发者需要对自己所保存的数据安全性负责，也不应索取其他应用的数据。
- `UserManager` 不应当处理游戏数据的格式问题，只负责读写。
- 所有函数都是 `async` 的。涉及文件读写时，应当使用 `aiofiles` 库。
- 为了避免写入数据时的并发问题，`UserManager` 可以使用 `asyncio.Lock` 来保护写入操作。这一过程对游戏开发者透明。

## `JSONUserManager` 示例

JSON 格式不适合用于存储大量数据，此处提供示例 `UserManager`，供开发者参考。

请参见 `gum/__init__.py`。
